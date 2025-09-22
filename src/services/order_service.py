# src/services/order_service.py
from src.services.customer_service import CustomerService, CustomerError
from src.services.product_service import ProductService, ProductError

class OrderError(Exception):
    pass

class OrderService:
    """Business logic for order management"""

    def __init__(self, customer_dao=None, product_dao=None):
        self.customer_service = CustomerService(dao=customer_dao)
        self.product_service = ProductService(dao=product_dao)
        self.orders = []
        self.next_id = 1

    def create_order(self, customer_id, items):
        # Check customer exists
        customer = None
        for c in self.customer_service.list_customers():
            if c["id"] == customer_id:
                customer = c
                break
        if not customer:
            raise OrderError(f"No customer found with id {customer_id}")

        # Validate stock and calculate total
        total_amount = 0
        for it in items:
            prod = self.product_service.get_product(it["prod_id"])
            if not prod:
                raise OrderError(f"Product id {it['prod_id']} does not exist")
            if prod["stock"] < it["quantity"]:
                raise OrderError(f"Not enough stock for '{prod['name']}'")
            total_amount += prod["price"] * it["quantity"]

        # Deduct stock
        for it in items:
            prod = self.product_service.get_product(it["prod_id"])
            prod["stock"] -= it["quantity"]

        # Save order
        order = {
            "id": self.next_id,
            "customer_id": customer_id,
            "items": items,
            "total_amount": total_amount,
            "status": "PLACED"
        }
        self.next_id += 1
        self.orders.append(order)
        customer["orders"].append(order["id"])
        return order

    def get_order_details(self, order_id):
        for o in self.orders:
            if o["id"] == order_id:
                customer = None
                for c in self.customer_service.list_customers():
                    if c["id"] == o["customer_id"]:
                        customer = c
                        break
                return {"order": o, "customer": customer}
        raise OrderError(f"No order found with id {order_id}")

    def list_orders_of_customer(self, customer_id):
        return [o for o in self.orders if o["customer_id"] == customer_id]

    def cancel_order(self, order_id):
        order = next((o for o in self.orders if o["id"] == order_id), None)
        if not order:
            raise OrderError(f"No order found with id {order_id}")
        if order["status"] != "PLACED":
            raise OrderError("Can cancel only orders with status = PLACED")
        for it in order["items"]:
            prod = self.product_service.get_product(it["prod_id"])
            prod["stock"] += it["quantity"]
        order["status"] = "CANCELLED"
        return order

    def complete_order(self, order_id):
        order = next((o for o in self.orders if o["id"] == order_id), None)
        if not order:
            raise OrderError(f"No order found with id {order_id}")
        if order["status"] != "PLACED":
            raise OrderError("Can complete only orders with status = PLACED")
        order["status"] = "COMPLETED"
        return order
