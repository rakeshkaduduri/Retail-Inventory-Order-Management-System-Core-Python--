# src/services/reporting_service.py
from typing import Optional, List, Dict
from src.dao.reporting_dao import ReportingDAO

class ReportingService:
    """Business logic for reports"""

    def __init__(self, dao: Optional[ReportingDAO] = None):
        self.dao = dao or ReportingDAO()

    def top_selling_products(self, limit: int = 5) -> List[Dict]:
        return self.dao.top_selling_products(limit=limit)

    def total_revenue_last_month(self) -> float:
        return self.dao.total_revenue_last_month()

    def orders_per_customer(self) -> List[Dict]:
        return self.dao.orders_per_customer()

    def frequent_customers(self) -> List[Dict]:
        return self.dao.frequent_customers()
