# # src/services/product_service.py
# from typing import List, Dict
# import src.dao.product_dao as product_dao
 
# class ProductError(Exception):
#     pass
 
# def add_product(name: str, sku: str, price: float, stock: int = 0, category: str | None = None) -> Dict:
#     """
#     Validate and insert a new product.
#     Raises ProductError on validation failure.
#     """
#     if price <= 0:
#         raise ProductError("Price must be greater than 0")
#     existing = product_dao.get_product_by_sku(sku)
#     if existing:
#         raise ProductError(f"SKU already exists: {sku}")
#     return product_dao.create_product(name, sku, price, stock, category)
 
# def restock_product(prod_id: int, delta: int) -> Dict:
#     if delta <= 0:
#         raise ProductError("Delta must be positive")
#     p = product_dao.get_product_by_id(prod_id)
#     if not p:
#         raise ProductError("Product not found")
#     new_stock = (p.get("stock") or 0) + delta
#     return product_dao.update_product(prod_id, {"stock": new_stock})
 
# def get_low_stock(threshold: int = 5) -> List[Dict]:
#     allp = product_dao.list_products(limit=1000)
#     return [p for p in allp if (p.get("stock") or 0) <= threshold]
 

# src/services/product_service.py
from typing import List, Dict, Optional
from src.dao.product_dao import ProductDAO


class ProductError(Exception):
    """Custom exception for product-related errors."""
    pass


class ProductService:
    """
    Service layer for business logic around Products.
    Uses ProductDAO for data access.
    """

    def __init__(self, dao: Optional[ProductDAO] = None):
        # Dependency Injection (default to new DAO if none passed)
        self.dao = dao or ProductDAO()

    def add_product(self, name: str, sku: str, price: float, stock: int = 0, category: Optional[str] = None) -> Dict:
        """
        Validate and insert a new product.
        Raises ProductError on validation failure.
        """
        if price <= 0:
            raise ProductError("Price must be greater than 0")

        existing = self.dao.get_product_by_sku(sku)
        if existing:
            raise ProductError(f"SKU already exists: {sku}")

        return self.dao.create_product(name, sku, price, stock, category)

    def restock_product(self, prod_id: int, delta: int) -> Dict:
        """
        Increase stock of a product by delta.
        """
        if delta <= 0:
            raise ProductError("Delta must be positive")

        p = self.dao.get_product_by_id(prod_id)
        if not p:
            raise ProductError("Product not found")

        new_stock = (p.get("stock") or 0) + delta
        return self.dao.update_product(prod_id, {"stock": new_stock})

    def get_low_stock(self, threshold: int = 5) -> List[Dict]:
        """
        Return products with stock <= threshold.
        """
        all_products = self.dao.list_products(limit=1000)
        return [p for p in all_products if (p.get("stock") or 0) <= threshold]

    def delete_product(self, prod_id: int) -> Optional[Dict]:
        """
        Delete a product by id and return deleted row.
        """
        return self.dao.delete_product(prod_id)

    def list_all_products(self, limit: int = 100, category: Optional[str] = None) -> List[Dict]:
        """
        List all products, optionally filtered by category.
        """
        return self.dao.list_products(limit=limit, category=category)
