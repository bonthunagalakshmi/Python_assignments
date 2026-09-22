from .base import BaseView, ttk


class DashboardView(BaseView):
    def build(self, parent):
        super().build(parent)
        self.title("Operations dashboard", "Live fleet and revenue signals from DriveEase_Data.xlsx")
        self.cards = ttk.Frame(self.frame)
        self.cards.pack(fill="x", pady=(0, 18))
        self.refresh()
        ttk.Label(
            self.frame,
            text="Use the navigation to register customers, manage vehicles, create date-based rentals, and close returns.",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(14, 0))
        return self.frame

    def refresh(self):
        if not self.cards:
            return
        for child in self.cards.winfo_children():
            child.destroy()
        summary = self.app.reports.dashboard_summary()
        labels = [
            ("Fleet", summary["total_vehicles"], "total_vehicles"),
            ("Available", summary["available"], "available"),
            ("Reserved", summary["reserved"], "reserved"),
            ("Rented", summary["rented"], "rented"),
            ("Maintenance", summary["maintenance"], "maintenance"),
            ("Revenue", f"₹{summary['revenue']:,.2f}", "revenue"),
        ]
        for index, (label, value, _) in enumerate(labels):
            card = ttk.Frame(self.cards, style="Metric.TFrame", padding=16)
            card.grid(row=0, column=index, padx=(0, 10), sticky="nsew")
            ttk.Label(card, text=label, style="Muted.TLabel").pack(anchor="w")
            ttk.Label(card, text=str(value), style="Metric.TLabel").pack(anchor="w", pady=(7, 0))
            self.cards.columnconfigure(index, weight=1)