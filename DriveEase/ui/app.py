from __future__ import annotations

from pathlib import Path

from data.excel_manager import ExcelManager
from services.customer_service import CustomerService
from services.fleet_service import FleetService
from services.maintenance_service import MaintenanceService
from services.payment_service import PaymentService
from services.pricing_service import PricingService
from services.rental_service import RentalService
from services.report_service import ReportService
from .base import tk, ttk
from .customer_view import CustomerView
from .dashboard import DashboardView
from .invoice_view import InvoiceView
from .maintenance_view import MaintenanceView
from .payment_view import PaymentView
from .rental_view import RentalView
from .report_view import ReportView
from .return_view import ReturnView
from .vehicle_view import VehicleView


class DriveEaseApp:
    def __init__(self, root, data_path: str | Path = "DriveEase_Data.xlsx"):
        if tk is None or ttk is None:
            raise RuntimeError("Tkinter is not available. Install a Python build with Tk support to launch the GUI.")
        self.root = root
        self.root.title("DriveEase | Vehicle Rental & Fleet Management")
        self.root.geometry("1280x760")
        self.root.minsize(1050, 650)
        self.excel = ExcelManager(data_path)
        self.customers = CustomerService(self.excel)
        self.fleet = FleetService(self.excel)
        self.pricing = PricingService()
        self.payments = PaymentService(self.excel)
        self.rentals = RentalService(self.excel, self.customers, self.fleet, self.pricing, self.payments)
        self.reports = ReportService(self.excel)
        self.maintenance = MaintenanceService(self.excel, self.fleet)
        self.views = {}
        self._configure_styles()
        self._build_shell()
        self.show_page("Dashboard")

    def _configure_styles(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass
        style.configure("Sidebar.TFrame", background="#12212b")
        style.configure("SidebarTitle.TLabel", background="#12212b", foreground="#f7f3eb", font=("TkDefaultFont", 17, "bold"))
        style.configure("Sidebar.TButton", background="#12212b", foreground="#d9e3e6", borderwidth=0, anchor="w", padding=(16, 10))
        style.map("Sidebar.TButton", background=[("active", "#1e3a47")], foreground=[("active", "#ffffff")])
        style.configure("PageTitle.TLabel", font=("TkDefaultFont", 24, "bold"), foreground="#12212b")
        style.configure("Muted.TLabel", foreground="#60727a")
        style.configure("Metric.TFrame", background="#e4f0ec", relief="flat")
        style.configure("Metric.TLabel", font=("TkDefaultFont", 19, "bold"), foreground="#12212b")
        style.configure("Accent.TButton", background="#176b5a", foreground="white", padding=(12, 7))
        style.map("Accent.TButton", background=[("active", "#115445")])
        style.configure("Report.TLabel", font=("TkDefaultFont", 12), foreground="#23343b")

    def _build_shell(self):
        self.sidebar = ttk.Frame(self.root, style="Sidebar.TFrame", width=220)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        ttk.Label(self.sidebar, text="DRIVEEASE", style="SidebarTitle.TLabel").pack(anchor="w", padx=16, pady=(24, 3))
        ttk.Label(self.sidebar, text="Rental office console", style="Sidebar.TLabel").pack(anchor="w", padx=16, pady=(0, 24))
        for name in ["Dashboard", "Customers", "Fleet", "New Rental", "Return Vehicle",
                     "Payments", "Invoices", "Reports", "Maintenance"]:
            ttk.Button(self.sidebar, text=name, style="Sidebar.TButton",
                       command=lambda page=name: self.show_page(page)).pack(fill="x")
        ttk.Label(self.sidebar, text="Excel-backed staff workspace", style="Sidebar.TLabel").pack(
            side="bottom", anchor="w", padx=16, pady=18
        )
        self.content = ttk.Frame(self.root)
        self.content.pack(side="left", fill="both", expand=True)

    def show_page(self, name: str):
        for child in self.content.winfo_children():
            child.destroy()
        page_classes = {
            "Dashboard": DashboardView, "Customers": CustomerView, "Fleet": VehicleView,
            "New Rental": RentalView, "Return Vehicle": ReturnView, "Payments": PaymentView,
            "Invoices": InvoiceView, "Reports": ReportView, "Maintenance": MaintenanceView,
        }
        view = self.views.get(name)
        if view is None or not isinstance(view, page_classes[name]):
            view = page_classes[name](self)
            self.views[name] = view
        view.build(self.content)
        self.active_view = view

    def refresh_all(self):
        for view in self.views.values():
            refresh = getattr(view, "refresh", None)
            if refresh:
                refresh()


def launch(data_path: str | Path = "DriveEase_Data.xlsx") -> None:
    if tk is None:
        raise RuntimeError("Tkinter is not available in this environment.")
    root = tk.Tk()
    DriveEaseApp(root, data_path)
    root.mainloop()