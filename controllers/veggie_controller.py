from flask import Blueprint, render_template,request,redirect
from config.db import SessionLocal
from models.veggie import Item,Veggie, UnitPriceVeggie, WeightedVeggie, PackVeggie, PremadeBox

veggie_bp = Blueprint('veggie', __name__)

# Veggie list route
@veggie_bp.route('/list')
def list():
    session = SessionLocal()
    try:
        # Query all veggies by their type
        
        unit_veggies = session.query(UnitPriceVeggie).all()

        weighted_veggies = session.query(WeightedVeggie).all()
        pack_veggies = session.query(PackVeggie).all()
        premade_boxes = session.query(PremadeBox).all()
        all_veggies = session.query(Item).filter(Item.type != 'premade_box').all()
       
        # Pass the data to the template
        return render_template(
            'veggie.html', 
            unit_veggies=unit_veggies,
            weighted_veggies=weighted_veggies,
            pack_veggies=pack_veggies,
            premade_boxes=premade_boxes,
            all_veggies = all_veggies
        )
    finally:
        session.close()
