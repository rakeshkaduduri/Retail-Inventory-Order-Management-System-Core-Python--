# # src/dao/product_dao.py
# from typing import Optional, List, Dict
# from src.config import get_supabase
 
# def _sb():
#     return get_supabase()
 
# def create_product(name: str, sku: str, price: float, stock: int = 0, category: str | None = None) -> Optional[Dict]:
#     """
#     Insert a product and return the inserted row (two-step: insert then select by unique sku).
#     """
#     payload = {"name": name, "sku": sku, "price": price, "stock": stock}
#     if category is not None:
#         payload["category"] = category
 
#     # Insert (no select chaining)
#     _sb().table("products").insert(payload).execute()
 
#     # Fetch inserted row by unique column (sku)
#     resp = _sb().table("products").select("*").eq("sku", sku).limit(1).execute()
#     return resp.data[0] if resp.data else None
 
# def get_product_by_id(prod_id: int) -> Optional[Dict]:
#     resp = _sb().table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
#     return resp.data[0] if resp.data else None
 
# def get_product_by_sku(sku: str) -> Optional[Dict]:
#     resp = _sb().table("products").select("*").eq("sku", sku).limit(1).execute()
#     return resp.data[0] if resp.data else None
 
# def update_product(prod_id: int, fields: Dict) -> Optional[Dict]:
#     """
#     Update and then return the updated row (two-step).
#     """
#     _sb().table("products").update(fields).eq("prod_id", prod_id).execute()
#     resp = _sb().table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
#     return resp.data[0] if resp.data else None
 
# def delete_product(prod_id: int) -> Optional[Dict]:
#     # fetch row before delete (so we can return it)
#     resp_before = _sb().table("products").select("*").eq("prod_id", prod_id).limit(1).execute()
#     row = resp_before.data[0] if resp_before.data else None
#     _sb().table("products").delete().eq("prod_id", prod_id).execute()
#     return row
 
# def list_products(limit: int = 100, category: str | None = None) -> List[Dict]:
#     q = _sb().table("products").select("*").order("prod_id", desc=False).limit(limit)
#     if category:
#         q = q.eq("category", category)
#     resp = q.execute()
#     return resp.data or []

from typing import Optional, List, Dict
from src.config import get_supabase


class ProductDAO:
    """DAO class for handling product database operations"""

    def __init__(self):
        self.sb = get_supabase()

    def create_product(
        self, name: str, sku: str, price: float, stock: int = 0, category: str | None = None
    ) -> Optional[Dict]:
        """
        Insert a product and return the inserted row (two-step: insert then select by unique sku).
        """
        payload = {"name": name, "sku": sku, "price": price, "stock": stock}
        if category is not None:
            payload["category"] = category

        # Insert
        self.sb.table("products").insert(payload).execute()

        # Fetch inserted row by unique SKU
        resp = (
            self.sb.table("products")
            .select("*")
            .eq("sku", sku)
            .limit(1)
            .execute()
        )
        return resp.data[0] if resp.data else None

    def get_product_by_id(self, prod_id: int) -> Optional[Dict]:
        resp = (
            self.sb.table("products")
            .select("*")
            .eq("prod_id", prod_id)
            .limit(1)
            .execute()
        )
        return resp.data[0] if resp.data else None

    def get_product_by_sku(self, sku: str) -> Optional[Dict]:
        resp = (
            self.sb.table("products")
            .select("*")
            .eq("sku", sku)
            .limit(1)
            .execute()
        )
        return resp.data[0] if resp.data else None

    def update_product(self, prod_id: int, fields: Dict) -> Optional[Dict]:
        """
        Update and then return the updated row (two-step).
        """
        self.sb.table("products").update(fields).eq("prod_id", prod_id).execute()
        resp = (
            self.sb.table("products")
            .select("*")
            .eq("prod_id", prod_id)
            .limit(1)
            .execute()
        )
        return resp.data[0] if resp.data else None

    def delete_product(self, prod_id: int) -> Optional[Dict]:
        # Fetch row before delete (so we can return it)
        resp_before = (
            self.sb.table("products")
            .select("*")
            .eq("prod_id", prod_id)
            .limit(1)
            .execute()
        )
        row = resp_before.data[0] if resp_before.data else None

        self.sb.table("products").delete().eq("prod_id", prod_id).execute()
        return row

    def list_products(self, limit: int = 100, category: str | None = None) -> List[Dict]:
        q = self.sb.table("products").select("*").order("prod_id", desc=False).limit(limit)
        if category:
            q = q.eq("category", category)
        resp = q.execute()
        return resp.data or []


if __name__ == "__main__":
    dao = ProductDAO()

    # Create a product
    prod = dao.create_product("Test Product", "SKU123", 199.99, 10, "Electronics")
    print("Inserted:", prod)

    # List products
    print("Products:", dao.list_products(limit=5))
