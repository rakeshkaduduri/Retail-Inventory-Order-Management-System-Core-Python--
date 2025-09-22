# src/dao/reporting_dao.py
from typing import List, Dict
from src.config import get_supabase

class ReportingDAO:
    """DAO for reporting queries"""

    def __init__(self):
        self.sb = get_supabase()

    def top_selling_products(self, limit: int = 5) -> List[Dict]:
        resp = self.sb.table("order_items").select("prod_id, quantity").execute()
        data = resp.data or []

        totals = {}
        for item in data:
            pid = item["prod_id"]
            qty = item["quantity"]
            totals[pid] = totals.get(pid, 0) + qty

        sorted_totals = sorted(totals.items(), key=lambda x: x[1], reverse=True)[:limit]
        products = []
        for pid, total_qty in sorted_totals:
            prod_resp = self.sb.table("products").select("*").eq("prod_id", pid).limit(1).execute()
            if prod_resp.data:
                prod = prod_resp.data[0]
                prod["total_sold"] = total_qty
                products.append(prod)
        return products

    def total_revenue_last_month(self) -> float:
        import datetime
        today = datetime.date.today()
        first_day_last_month = (today.replace(day=1) - datetime.timedelta(days=1)).replace(day=1)
        last_day_last_month = today.replace(day=1) - datetime.timedelta(days=1)

        resp = self.sb.table("payments").select("amount").gte("created_at", str(first_day_last_month)) \
            .lte("created_at", str(last_day_last_month)).eq("status", "PAID").execute()
        data = resp.data or []
        return sum(item["amount"] for item in data)

    def orders_per_customer(self) -> List[Dict]:
        resp = self.sb.table("orders").select("customer_id").execute()
        counts = {}
        for o in resp.data or []:
            cid = o["customer_id"]
            counts[cid] = counts.get(cid, 0) + 1

        result = []
        for cid, total_orders in counts.items():
            cust_resp = self.sb.table("customers").select("*").eq("id", cid).limit(1).execute()
            if cust_resp.data:
                customer = cust_resp.data[0]
                customer["total_orders"] = total_orders
                result.append(customer)
        return result

    def frequent_customers(self, min_orders: int = 3) -> List[Dict]:
        all_customers = self.orders_per_customer()
        return [c for c in all_customers if c.get("total_orders", 0) >= min_orders]
