
import sys
import os

# Append the parent directory to the system path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.db import Base, engine
from models.person import Person, Customer, CorporateCustomer, Staff
from models.order import Order
from models.orderline import OrderLine
from models.veggie import Item, Veggie, WeightedVeggie, PackVeggie, UnitPriceVeggie, PremadeBox
from models.payment import Payment,DebitCardPayment,CreditCardPayment

def create_or_replace_tables():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("Tables recreated successfully.")

if __name__ == "__main__":
    create_or_replace_tables()