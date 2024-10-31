from sqlalchemy import Column, Integer, String, Float, ForeignKey,Date
from sqlalchemy.orm import relationship
from config.db import Base
from models.order import Order  # Make sure the path is correct
from models.orderline import OrderLine
from models.payment import Payment,DebitCardPayment,CreditCardPayment

class Person(Base):
    __tablename__ = 'person'
    
    id = Column(Integer, primary_key=True)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

        # type column to distinguish staff and customers
    type = Column(String(50), nullable=False)  # e.g., 'customer', 'staff', 'corporate_customer'

    __mapper_args__ = {
        'polymorphic_identity': 'person',
        'polymorphic_on': type  # Polymorphism to allow different types of customers
    }
    def __init__(self, first_name, last_name, username, password, type):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.type = type

    def __str__(self):
        return f"Person(ID={self.id}, Username={self.username}, Role={self.type})"


class Customer(Person):
    __tablename__ = 'customer'
    
    customer_id = Column(Integer, ForeignKey('person.id'), primary_key=True)
    cust_address = Column(String(100))
    cust_balance = Column(Float, default=0.0)
    max_owing = Column(Float)
      # Foreign key to Staff to represent the staff managing this customer
    staff_id = Column(Integer, ForeignKey('staff.staff_id'))  # Add the foreign key to link with Staff
        # Define the many-to-one relationship (many customers can be managed by one staff member)

    staff = relationship('Staff', back_populates='list_of_customers', foreign_keys=[staff_id])  # Specify the correct foreign key
    list_of_orders = relationship('Order', back_populates='customer')  # Make sure this exists
    # Relationship to Payment
    list_of_payments = relationship('Payment', back_populates='customer')


    __mapper_args__ = {
        'polymorphic_identity': 'customer',
    }

    def __init__(self, first_name, last_name, username, password, cust_address, cust_balance=0.0, max_owing=None, staff_id=None):
        super().__init__(first_name, last_name, username, password, type='customer')
        self.cust_address = cust_address
        self.cust_balance = cust_balance
        self.max_owing = max_owing
        self.staff_id = staff_id

    def __str__(self):
        return f"Customer(ID={self.customer_id}, Address={self.cust_address}, Balance={self.cust_balance}, Staff ID={self.staff_id})"

class CorporateCustomer(Customer):
    __tablename__ = 'corporate_customer'
    
    corporate_customer_id = Column(Integer, ForeignKey('customer.customer_id'), primary_key=True)
    discount_rate = Column(Float)
    max_credit = Column(Float)
    min_balance = Column(Float)

    __mapper_args__ = {
        'polymorphic_identity': 'corporate_customer',  # Use a unique identity for CorporateCustomer
    }

    def __init__(self, first_name, last_name, username, password, cust_address, cust_balance=0.0, max_owing=None, staff_id=None, discount_rate=None, max_credit=None, min_balance=None):
        # Call the parent (Customer) constructor explicitly
        super().__init__(first_name, last_name, username, password, cust_address, cust_balance, max_owing, staff_id)
        self.discount_rate = discount_rate
        self.max_credit = max_credit
        self.min_balance = min_balance
        self.type = 'corporate_customer'  # Automatically set the type to 'corporate_customer'

  
    def __str__(self):
        return f"CorporateCustomer(ID={self.corporate_customer_id}, Discount Rate={self.discount_rate}, Max Credit={self.max_credit})"


class Staff(Person):
    __tablename__ = 'staff'

    # Unique ID for the staff member (inherited from Person)
    staff_id = Column(Integer, ForeignKey('person.id'), primary_key=True)

    # Date when the staff member joined the company
    date_joined = Column(Date, nullable=False)

    # Name of the department where the staff member works (e.g., Sales, Support, Operations)
    dept_name = Column(String(100), nullable=False)

    # Relationship: This represents a list of customers assigned to the staff member.
    # One-to-Many relationship: One staff member can have many customers
    list_of_customers = relationship('Customer', back_populates='staff', foreign_keys=[Customer.staff_id])  # Specify the correct foreign key

    # Relationship: This represents a list of orders that the staff member is associated with.
    # One-to-Many relationship: One staff member can manage multiple orders.
    list_of_orders = relationship('Order', back_populates='staff')

    # Relationship: This represents a list of premade boxes handled or created by the staff member.
    # One-to-Many relationship: One staff member can manage multiple premade boxes.
    premade_boxes = relationship('PremadeBox', back_populates='staff')

    # Relationship: This represents the list of veggies that the staff member interacts with.
    # One-to-Many relationship: One staff member can manage multiple veggies.
    veggies = relationship('Veggie', back_populates='staff')
   

    __mapper_args__ = {
        'polymorphic_identity': 'staff',
    }
    def __init__(self, first_name, last_name, username, password, date_joined, dept_name):
        # Call the parent (Person) constructor explicitly
        super().__init__(first_name, last_name, username, password, type='staff')
        self.date_joined = date_joined
        self.dept_name = dept_name
    
    def __str__(self):
        """String representation of the Staff object for easy display."""
        return f"Staff(ID={self.staff_id}, Dept={self.dept_name}, Date Joined={self.date_joined})"
