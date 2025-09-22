# src/services/payment_service.py
from src.dao.payment_dao import PaymentDAO

class PaymentError(Exception):
    pass

class PaymentService:
    def __init__(self, dao=None):
        self.dao = dao or PaymentDAO()

    def create_payment(self, order_id: int, amount: float):
        return self.dao.create_payment(order_id, amount)

    def process_payment(self, order_id: int, method: str):
        if method not in ["Cash", "Card", "UPI"]:
            raise PaymentError("Invalid payment method")
        return self.dao.mark_paid(order_id, method)

    def refund_payment(self, order_id: int):
        return self.dao.mark_refunded(order_id)

    def get_payment_status(self, order_id: int):
        return self.dao.get_payment(order_id)
