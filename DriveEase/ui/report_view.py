from .base import BaseView, ttk


class ReportView(BaseView):
    def build(self, parent):
        super().build(parent)
        self.title("Reports", "Live summaries calculated from the current Excel workbook.")
        self.report_text = ttk.Label(self.frame, justify="left", style="Report.TLabel")
        self.report_text.pack(anchor="w")
        ttk.Button(self.frame, text="Refresh reports", command=self.refresh).pack(anchor="w", pady=16)
        self.refresh()
        return self.frame

    def refresh(self):
        if not hasattr(self, "report_text"):
            return
        summary = self.app.reports.dashboard_summary()
        by_type = self.app.reports.revenue_by_vehicle_type() or {"—": 0}
        by_method = self.app.reports.revenue_by_payment_method() or {"—": 0}
        top = self.app.reports.most_rented_vehicles()[:5] or [{"vehicle_id": "—", "rental_count": 0}]
        most_rented = ", ".join(
            f"{row['vehicle_id']} ({row['rental_count']})" for row in top
        )
        text = (
            f"Fleet utilization\n\n"
            f"Vehicles: {summary['total_vehicles']}    Available: {summary['available']}    "
            f"Reserved: {summary['reserved']}    Rented: {summary['rented']}    "
            f"Maintenance: {summary['maintenance']}\n"
            f"Active rentals: {summary['active_rentals']}    Recorded revenue: ₹{summary['revenue']:,.2f}\n\n"
            f"Revenue by vehicle type: {', '.join(f'{key} ₹{value:,.2f}' for key, value in by_type.items())}\n"
            f"Revenue by payment method: {', '.join(f'{key} ₹{value:,.2f}' for key, value in by_method.items())}\n\n"
            f"Most rented: {most_rented}"
        )
        self.report_text.configure(text=text)