# src/dao/payment_dao.py
from typing import Optional, Dict, List
from src.config import get_supabase

class PaymentDAO:
    def __init__(self):
        self.sb = get_supabase()

    def create_payment(self, order_id: int, amount: float) -> Optional[Dict]:
        payload = {"order_id": order_id, "amount": amount, "status": "PENDING", "method": None}
        self.sb.table("payments").insert(payload).execute()
        resp = self.sb.table("payments").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def mark_paid(self, order_id: int, method: str) -> Optional[Dict]:
        self.sb.table("payments").update({"status": "PAID", "method": method}).eq("order_id", order_id).execute()
        resp = self.sb.table("payments").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def mark_refunded(self, order_id: int) -> Optional[Dict]:
        self.sb.table("payments").update({"status": "REFUNDED"}).eq("order_id", order_id).execute()
        resp = self.sb.table("payments").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_payment(self, order_id: int) -> Optional[Dict]:
        resp = self.sb.table("payments").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None
