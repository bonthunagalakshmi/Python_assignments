from __future__ import annotations

try:
    import tkinter as tk
    from tkinter import messagebox, ttk
except ImportError:  # Allows domain imports and compile checks on headless Python builds.
    tk = None
    ttk = None
    messagebox = None


class BaseView:
    def __init__(self, app):
        self.app = app
        self.frame = None

    def build(self, parent):
        if ttk is None:
            raise RuntimeError("Tkinter is not available in this Python environment.")
        self.frame = ttk.Frame(parent, padding=24)
        self.frame.pack(fill="both", expand=True)
        return self.frame

    def title(self, text: str, subtitle: str = "") -> None:
        ttk.Label(self.frame, text=text, style="PageTitle.TLabel").pack(anchor="w")
        if subtitle:
            ttk.Label(self.frame, text=subtitle, style="Muted.TLabel").pack(anchor="w", pady=(4, 18))

    def tree(self, columns: list[tuple[str, str, int]]) -> ttk.Treeview:
        wrapper = ttk.Frame(self.frame)
        wrapper.pack(fill="both", expand=True, pady=(14, 0))
        tree = ttk.Treeview(wrapper, columns=[c[0] for c in columns], show="headings")
        for column, label, width in columns:
            tree.heading(column, text=label)
            tree.column(column, width=width, anchor="w")
        scroll = ttk.Scrollbar(wrapper, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scroll.set)
        tree.pack(side="left", fill="both", expand=True)
        scroll.pack(side="right", fill="y")
        return tree

    @staticmethod
    def clear_tree(tree) -> None:
        for item in tree.get_children():
            tree.delete(item)

    def error(self, error: Exception) -> None:
        if messagebox:
            messagebox.showerror("DriveEase", str(error), parent=self.app.root)

    def info(self, message: str) -> None:
        if messagebox:
            messagebox.showinfo("DriveEase", message, parent=self.app.root)