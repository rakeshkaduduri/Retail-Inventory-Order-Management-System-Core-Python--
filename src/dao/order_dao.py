# src/dao/order_dao.py

class OrderDAO:
    """Handles orders storage"""

    def __init__(self):
        self.orders = []
        self.next_id = 1

    def save_order(self, order):
        order["id"] = self.next_id
        self.next_id += 1
        self.orders.append(order)
        return order

    def find_by_id(self, order_id):
        for o in self.orders:
            if o["id"] == order_id:
                return o
        return None

    def list_orders(self):
        return self.orders
