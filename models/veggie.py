# models/veggie.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table,UniqueConstraint
from sqlalchemy.orm import relationship
from config.db import Base


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    type = Column(String(50), nullable=False)  # Polymorphic discriminator column
    # Relationship to OrderLine
    orderlines = relationship('OrderLine', back_populates='item')

    __mapper_args__ = {
        'polymorphic_identity': 'item',
        'polymorphic_on': type  # For polymorphism
    }

    def __init__(self, name, type):  # Ensure constructor accepts both 'name' and 'type'
        self.name = name
        self.type = type  # Set the type when initializing

class Veggie(Item):
    __tablename__ = 'veggies'
    id = Column(Integer, ForeignKey('items.id'), primary_key=True)
    staff_id = Column(Integer, ForeignKey('staff.staff_id'))  # Link each veggie to a staff member
        # Add cascade to allow automatic deletion of related records
    # Back-reference to Staff

    staff = relationship('Staff', back_populates='veggies')
    # Many-to-many relationship with PremadeBox
    premade_boxes = relationship('PremadeBox', secondary='box_veggie_link', back_populates='box_content')

    __mapper_args__ = {
        'polymorphic_identity': 'veggie',
        'polymorphic_on': Item.type  # Polymorphic on Item's type column

    }

    def __init__(self, name,type):
        super().__init__(name,type)  # Pass 'name' and 'veggie' as type to Item

class WeightedVeggie(Veggie):
    __tablename__ = 'weighted_veggies' 
    id = Column(Integer, ForeignKey('veggies.id'), primary_key=True)
    weight = Column(Float, nullable=False)
    weightPerKilo = Column(Float, nullable=False)  # Keep 'weightPerKilo'

    __mapper_args__ = {
        'polymorphic_identity': 'weighted_veggie',  # Ensure identity is set
    }

    def __init__(self, name, weight, weightPerKilo):
        super().__init__(name,'weighted_veggie')  # Pass 'name' to Veggie
        self.weight = weight
        self.weightPerKilo = weightPerKilo


class PackVeggie(Veggie):
    __tablename__ = 'pack_veggies'
    id = Column(Integer, ForeignKey('veggies.id'), primary_key=True)
    numOfPack = Column(Integer, nullable=False)  # Keep 'numOfPack'
    pricePerPack = Column(Float, nullable=False)  # Keep 'pricePerPack'

    __mapper_args__ = {
        'polymorphic_identity': 'pack_veggie',
    }

    def __init__(self, name, numOfPack, pricePerPack):
        super().__init__(name,'pack_veggie')  # Pass 'name' to Veggie
        self.numOfPack = numOfPack
        self.pricePerPack = pricePerPack

class UnitPriceVeggie(Veggie):
    __tablename__ = 'unit_veggies'

    id = Column(Integer, ForeignKey('veggies.id'), primary_key=True)
    pricePerUnit = Column(Float, nullable=False)  # Keep 'pricePerUnit'
    quantity = Column(Integer, nullable=False)  # Keep 'quantity'

    __mapper_args__ = {
        'polymorphic_identity': 'unit_veggie',
    }

    def __init__(self, name, pricePerUnit, quantity):
        # Initialize the Veggie class (which calls the Item class constructor)
        super().__init__(name,'unit_veggie')  # No need to pass type here because the parent class sets it to 'veggie'
        self.pricePerUnit = pricePerUnit
        self.quantity = quantity

# PremadeBox class, inheriting from Item
class PremadeBox(Item):
    __tablename__ = 'premade_boxes'

    # Inherits the item_id (primary key) from Item class
    item_id = Column(Integer, ForeignKey('items.id'), primary_key=True)

    # Fields specific to PremadeBox
    box_size = Column(String(20), nullable=False)  # small, medium, large
    num_of_boxes = Column(Integer, nullable=False)
    box_price = Column(Float)

    # Many-to-many relationship with Veggie
    box_content = relationship('Veggie', secondary='box_veggie_link', back_populates='premade_boxes')

    # Relationship with Staff (if needed)
    staff_id = Column(Integer, ForeignKey('staff.staff_id'))
    staff = relationship('Staff', back_populates='premade_boxes')

    __mapper_args__ = {
        'polymorphic_identity': 'premade_box',  # Ensure the identity is set
    }

    def __init__(self, box_size, num_of_boxes, staff_id=None):
            # Set the item name dynamically based on the box size
        name = f"Premade Box ({box_size.capitalize()})"

        super().__init__(name=name, type='premade_box')  # Pass name and type to Item
        self.box_size = box_size
        self.num_of_boxes = num_of_boxes
        self.staff_id = staff_id
        self.box_price = self.calculate_box_price()

    def calculate_box_price(self):
        """Method to calculate box price based on box size."""
        if self.box_size == 'small':
            return 10.00
        elif self.box_size == 'medium':
            return 20.00
        elif self.box_size == 'large':
            return 30.00
        return 0

    def __str__(self):
        return f"PremadeBox({self.item_id}, {self.box_size}, {self.num_of_boxes}, {self.box_price})"


# Many-to-many relationship table for veggies and premade boxes
box_veggie_link = Table('box_veggie_link', Base.metadata,
    Column('box_id', Integer, ForeignKey('premade_boxes.item_id')),
    Column('veggie_id', Integer, ForeignKey('veggies.id')),
    UniqueConstraint('box_id', 'veggie_id', name='uq_box_veggie_link')  # Ensure uniqueness in many-to-many relationships
)
