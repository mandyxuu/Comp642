from sqlalchemy import Column, Integer, ForeignKey,Float,String
from sqlalchemy.orm import relationship
from config.db import Base

class OrderLine(Base):
    __tablename__ = 'orderline'

    orderline_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('order.order_id'))  # Foreign key to Order
    item_id = Column(Integer, ForeignKey('items.id'))  # Foreign key to Item
    item_type = Column(String(50), nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
  # Columns to store up to 4 selected items for premade boxes
    # Selected items for premade boxes (not foreign keys)
    selected_item_1 = Column(Integer, nullable=True)  # No foreign key constraint
    selected_item_2 = Column(Integer, nullable=True)
    selected_item_3 = Column(Integer, nullable=True)
    selected_item_4 = Column(Integer, nullable=True)

    # Relationships
    # item = relationship('Item', foreign_keys=[item_id], back_populates='orderlines')
    # selected_items = relationship('Item', foreign_keys=[selected_item_1, selected_item_2, selected_item_3, selected_item_4])
    # order = relationship('Order', back_populates='list_of_items')

    # # Relationships
    item = relationship('Item', back_populates='orderlines')
    order = relationship('Order', back_populates='list_of_items')

    def __init__(self, order_id, item_id, item_type, quantity, price, total_price,
                 selected_item_1=None, selected_item_2=None, selected_item_3=None, selected_item_4=None):
        self.order_id = order_id
        self.item_id = item_id
        self.item_type = item_type
        self.quantity = quantity
        self.price = price
        self.total_price = total_price
        self.selected_item_1 = selected_item_1
        self.selected_item_2 = selected_item_2
        self.selected_item_3 = selected_item_3
        self.selected_item_4 = selected_item_4

    def __str__(self):
        """String representation of the OrderLine object for easy display."""
        selected_items = [
            self.selected_item_1,
            self.selected_item_2,
            self.selected_item_3,
            self.selected_item_4
        ]
        # Filter out None values and join selected item IDs as a comma-separated string
        selected_items_str = ", ".join(str(item) for item in selected_items if item is not None)
        
        return (f"OrderLine(ID={self.orderline_id}, Order ID={self.order_id}, "
                f"Item ID={self.item_id}, Item Type={self.item_type}, "
                f"Quantity={self.quantity}, Price={self.price}, Total Price={self.total_price}, "
                f"Selected Items=[{selected_items_str}])")
