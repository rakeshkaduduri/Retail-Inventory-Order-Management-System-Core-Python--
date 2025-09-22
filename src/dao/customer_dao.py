# src/dao/customer_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase

class CustomerDAO:
    """DAO for handling customers in Supabase"""

    def __init__(self):
        self.sb = get_supabase()

    def create_customer(self, name: str, email: str, phone: str, city: Optional[str] = None) -> Optional[Dict]:
        payload = {"name": name, "email": email, "phone": phone, "city": city}

        # Insert into Supabase
        self.sb.table("customers").insert(payload).execute()

        # Fetch inserted customer by unique email
        resp = self.sb.table("customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    def find_by_email(self, email: str) -> Optional[Dict]:
        resp = self.sb.table("customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update_customer(self, email: str, fields: Dict) -> Optional[Dict]:
        self.sb.table("customers").update(fields).eq("email", email).execute()
        resp = self.sb.table("customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete_customer(self, email: str) -> bool:
        self.sb.table("customers").delete().eq("email", email).execute()
        return True

    def list_customers(self) -> List[Dict]:
        resp = self.sb.table("customers").select("*").order("id", desc=False).execute()
        return resp.data or []

    def search_customers(self, email: Optional[str] = None, city: Optional[str] = None) -> List[Dict]:
        q = self.sb.table("customers").select("*")
        if email:
            q = q.eq("email", email)
        if city:
            q = q.eq("city", city)
        resp = q.execute()
        return resp.data or []
