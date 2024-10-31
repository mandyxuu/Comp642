from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from config.db import Base

class Payment(Base):
    __tablename__ = 'payment'

    payment_id = Column(Integer, primary_key=True)
    payment_amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False)
    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    order_id = Column(Integer, ForeignKey('order.order_id'))  # Link payment to a specific order

    is_delivery = Column(Boolean, nullable=False, default=False)
    payment_type = Column(String(50))  # Column to indicate the type of payment

    # Relationships
    customer = relationship('Customer', back_populates='list_of_payments')
    order = relationship('Order', back_populates='payments')  # Link payment to order

    __mapper_args__ = {
        'polymorphic_on': payment_type,  # Use payment_type to determine subclass
        'polymorphic_identity': 'payment'
    }

    def __init__(self, payment_amount, payment_date, customer_id, order_id, is_delivery=False):
        self.payment_amount = payment_amount
        self.payment_date = payment_date
        self.customer_id = customer_id
        self.order_id = order_id
        self.is_delivery = is_delivery

    def __str__(self):
        return (f"Payment(ID={self.payment_id}, Amount={self.payment_amount}, "
                f"Date={self.payment_date}, Customer ID={self.customer_id}, "
                f"Order ID={self.order_id}, Delivery={self.is_delivery})")

class CreditCardPayment(Payment):
    __tablename__ = 'credit_card_payment'

    payment_id = Column(Integer, ForeignKey('payment.payment_id'), primary_key=True)
    card_expiry_date = Column(String(10))
    card_number = Column(String(16), nullable=False)
    card_type = Column(String(10))

    __mapper_args__ = {
        'polymorphic_identity': 'credit_card_payment',
        'inherit_condition': payment_id == Payment.payment_id
    }

    def __init__(self, payment_amount, payment_date, customer_id, order_id, card_expiry_date, card_number, card_type, is_delivery=False):
        super().__init__(payment_amount, payment_date, customer_id, order_id, is_delivery)
        self.card_expiry_date = card_expiry_date
        self.card_number = card_number
        self.card_type = card_type

    def __str__(self):
        return (f"CreditCardPayment(ID={self.payment_id}, Amount={self.payment_amount}, "
                f"Date={self.payment_date}, Card Number={self.card_number}, "
                f"Expiry Date={self.card_expiry_date}, Card Type={self.card_type})")

class DebitCardPayment(Payment):
    __tablename__ = 'debit_card_payment'

    payment_id = Column(Integer, ForeignKey('payment.payment_id'), primary_key=True)
    bank_name = Column(String(50))
    debit_card_number = Column(String(16))

    __mapper_args__ = {
        'polymorphic_identity': 'debit_card_payment',
        'inherit_condition': payment_id == Payment.payment_id
    }

    def __init__(self, payment_amount, payment_date, customer_id, order_id, bank_name, debit_card_number, is_delivery=False):
        super().__init__(payment_amount, payment_date, customer_id, order_id, is_delivery)
        self.bank_name = bank_name
        self.debit_card_number = debit_card_number

    def __str__(self):
        return (f"DebitCardPayment(ID={self.payment_id}, Amount={self.payment_amount}, "
                f"Date={self.payment_date}, Bank Name={self.bank_name}, "
                f"Debit Card Number={self.debit_card_number})")
