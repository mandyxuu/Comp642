from sqlalchemy import Column, Integer, String, ForeignKey,DateTime,Float,Boolean
from sqlalchemy.orm import relationship
from config.db import Base
from models.orderline import OrderLine

class Order(Base):
    __tablename__ = 'order'

    order_id = Column(Integer, primary_key=True)
    order_date = Column(DateTime, nullable=False)
    order_status = Column(String(50), nullable=False)

    customer_id = Column(Integer, ForeignKey('customer.customer_id'))
    staff_id = Column(Integer, ForeignKey('staff.staff_id'))
    total_amount = Column(Float, nullable=False, default=0.0)


      # Use string-based reference for OrderLine

    list_of_items = relationship('OrderLine', back_populates='order')
    # Define the relationship to Customer

    customer = relationship('Customer', back_populates='list_of_orders')
    # Relationship back to staff
    staff = relationship('Staff', back_populates='list_of_orders')
    payments = relationship("Payment", back_populates="order")


    def __init__(self, order_date, order_status,total_amount, customer_id=None, staff_id=None):
        self.order_date = order_date
        self.order_status = order_status
        self.total_amount = total_amount

        self.customer_id = customer_id
        self.staff_id = staff_id

    def __str__(self):
        """String representation of the Order object for easy display."""
        return (f"Order(ID={self.order_id}, Date={self.order_date}, "
                f"Amount={self.total_amount}, Status={self.order_status}, "
                f"Customer ID={self.customer_id}, Staff ID={self.staff_id})")
