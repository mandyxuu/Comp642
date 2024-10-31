from sqlalchemy.orm import Session
from config.db import SessionLocal, engine, Base
from models.orderline import OrderLine
from models.payment import Payment,DebitCardPayment,CreditCardPayment
from models.order import Order
from models.person import Person, Customer, CorporateCustomer, Staff
from models.veggie import Item, Veggie, WeightedVeggie, PackVeggie, UnitPriceVeggie, PremadeBox
from  datetime import date
import hashlib

# Hash function for password
def hash_password(plaintext_password):
    return hashlib.sha256(plaintext_password.encode('utf-8')).hexdigest()

# Insert users (customers and staff)
def insert_users():
    session = SessionLocal()
    try:
        # Hashed password (comp123) for all users
        hashed_password = hash_password("comp123")
        
        # Add 5 customers to both person and customer tables
        customers = [
            Customer(first_name="John", last_name="Doe", username="johndoe", password=hashed_password, cust_address="123 Street A", cust_balance=0, max_owing=100.0),
            Customer(first_name="Jane", last_name="Smith", username="janesmith", password=hashed_password, cust_address="456 Street B", cust_balance=0, max_owing=100.0),
            Customer(first_name="Emily", last_name="Clark", username="emilyclark", password=hashed_password, cust_address="789 Street C", cust_balance=0, max_owing=100.0),
            Customer(first_name="Michael", last_name="Brown", username="michaelbrown", password=hashed_password, cust_address="321 Street D", cust_balance=0, max_owing=100.0),
            Customer(first_name="Olivia", last_name="Green", username="oliviagreen", password=hashed_password, cust_address="654 Street E", cust_balance=0, max_owing=100.0)
        ]
        
        # Add 2 corporate customers (username, password in person; specific fields in corporate_customer)
        corporate_customers = [
            CorporateCustomer(first_name="David", last_name="Johnson", username="davidjohnson", password=hashed_password, cust_address="111 Corporate Lane", cust_balance=0, max_owing=1000.0, discount_rate=10, max_credit=25000.0, min_balance=0.0),
            CorporateCustomer(first_name="Sarah", last_name="Wilson", username="sarahwilson", password=hashed_password, cust_address="222 Corporate Lane", cust_balance=0, max_owing=1000.0, discount_rate=10, max_credit=30000.0, min_balance=0.0)
        ]
        
        # Add 2 staff members (username and password in person; date_joined, dept_name in staff)
        staff = [
            Staff(first_name="Laura", last_name="Adams", username="lauraadams", password=hashed_password, date_joined=date(2023, 1, 15), dept_name="Sales"),
            Staff(first_name="Mark", last_name="Thomas", username="markthomas", password=hashed_password, date_joined=date(2023, 3, 1), dept_name="Support")
        ]
        
        # Add all data to session
        session.add_all(customers + corporate_customers + staff)
        session.commit()
        print("Data inserted successfully into Person, Customer, CorporateCustomer, and Staff tables.")
    
    except Exception as e:
        session.rollback()
        print(f"Error inserting data: {e}")
    finally:
        session.close()


# Insert items: veggies, packs, weights, units, and premade boxes
def insert_items():
    session = SessionLocal()
    try:
        
        # Insert WeightedVeggie
        weighted_veggies = [
            WeightedVeggie(name='Spinach',  weight=2.0, weightPerKilo=4.0),
            WeightedVeggie(name='Lettuce', weight=1.5, weightPerKilo=3.0),
            WeightedVeggie(name='Kale', weight=2.2, weightPerKilo=4.5),
            WeightedVeggie(name='Arugula',  weight=1.0, weightPerKilo=5.0),
            WeightedVeggie(name='Collard Greens', weight=1.8, weightPerKilo=3.5)
        ]
        
        # Insert PackVeggie
        pack_veggies = [
            PackVeggie(name='Carrot Pack', numOfPack=5, pricePerPack=7.0),
            PackVeggie(name='Potato Pack', numOfPack=4, pricePerPack=6.0),
            PackVeggie(name='Beetroot Pack', numOfPack=6, pricePerPack=8.0),
            PackVeggie(name='Turnip Pack', numOfPack=5, pricePerPack=7.5),
            PackVeggie(name='Radish Pack', numOfPack=3, pricePerPack=5.5)
        ]
        
        # Insert UnitPriceVeggie
        unit_veggies = [
            UnitPriceVeggie(name='Pumpkin', pricePerUnit=6.0, quantity=1),
            UnitPriceVeggie(name='Corn Cob', pricePerUnit=3.0, quantity=4),
            UnitPriceVeggie(name='Butternut Squash',  pricePerUnit=7.0, quantity=1),
            UnitPriceVeggie(name='Zucchini', pricePerUnit=2.0, quantity=5),
            UnitPriceVeggie(name='Sweet Potato', pricePerUnit=4.0, quantity=2)
        ]
        
        # Insert PremadeBox
        box_small = PremadeBox( box_size='small', num_of_boxes=4)
        box_medium = PremadeBox( box_size='medium', num_of_boxes=4)
        box_large = PremadeBox( box_size='large', num_of_boxes=4)
        

        # Link veggies to the premade boxes
        box_small.boxContent = weighted_veggies[:2]  # Add two weighted veggies
        box_medium.boxContent = weighted_veggies + pack_veggies[:2]  # Add more veggies
        box_large.boxContent = weighted_veggies + pack_veggies + unit_veggies  # Add all types

        # Add all veggies and boxes to session
        session.add_all(weighted_veggies + pack_veggies + unit_veggies + [box_small, box_medium, box_large])
        session.commit()
        print("Items (veggies and premade boxes) added successfully!")
    
    except Exception as e:
        session.rollback()
        print(f"Error inserting items: {e}")
    finally:
        session.close()

if __name__ == '__main__':
    insert_users()
    insert_items()
