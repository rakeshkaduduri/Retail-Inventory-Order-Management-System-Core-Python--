# src/services/customer_service.py
from src.dao.customer_dao import CustomerDAO
from typing import Optional, List, Dict

class CustomerError(Exception):
    pass

class CustomerService:
    """Business logic for customers"""

    def __init__(self, dao: Optional[CustomerDAO] = None):
        self.dao = dao or CustomerDAO()

    def add_customer(self, name: str, email: str, phone: str, city: Optional[str] = None) -> Dict:
        if self.dao.find_by_email(email):
            raise CustomerError(f"Email '{email}' already exists!")
        return self.dao.create_customer(name, email, phone, city)

    def update_customer(self, email: str, phone: Optional[str] = None, city: Optional[str] = None) -> Dict:
        customer = self.dao.find_by_email(email)
        if not customer:
            raise CustomerError(f"No customer found with email '{email}'")
        fields = {}
        if phone:
            fields["phone"] = phone
        if city:
            fields["city"] = city
        return self.dao.update_customer(email, fields)

    def delete_customer(self, email: str) -> bool:
        customer = self.dao.find_by_email(email)
        if not customer:
            raise CustomerError(f"No customer found with email '{email}'")
        # Check orders if you have orders table
        # if customer.get("orders"):
        #     raise CustomerError("Cannot delete customer with orders")
        return self.dao.delete_customer(email)

    def list_customers(self) -> List[Dict]:
        return self.dao.list_customers()

    def search_customers(self, email: Optional[str] = None, city: Optional[str] = None) -> List[Dict]:
        return self.dao.search_customers(email=email, city=city)
