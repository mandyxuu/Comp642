import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
from flask import Blueprint, render_template
from config.db import SessionLocal
from models.veggie import Item,Veggie, UnitPriceVeggie, WeightedVeggie, PackVeggie, PremadeBox
session = SessionLocal()
session = SessionLocal()

# Insert a WeightedVeggie and check its type
weighted_veggie = WeightedVeggie(name='Spinach', weight=2.0, weightPerKilo=4.0)
session.add(weighted_veggie)
session.commit()

# Query the item and print its details
item = session.query(Item).filter_by(name='Spinach').first()
print(f"Item: {item.name}, Type: {item.type}, Class: {type(item).__name__}")
for veggie in weighted_veggies:
    print(f"Inserting: {veggie.name}, Type: {veggie.type}")  # Check the type before commit
    session.add(veggie)
session.commit()
