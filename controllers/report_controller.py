
from flask import Blueprint, render_template
from sqlalchemy import func
import datetime
from models.person import Person,Customer,CorporateCustomer
from models.order import Order
from models.orderline import OrderLine
from models.veggie import Veggie,Item
from config.db import SessionLocal

report_bp = Blueprint('report', __name__)

@report_bp.route('/report')
def report():
    session = SessionLocal()

    # Generate a list of all customers
    customers= session.query(Person,Customer).join(Customer).all()

    # Generate total sales for the week, month, and year
    sales_totals = get_sales_totals(session)

    # Get the most popular items
    popular_items = get_most_popular_items(session)

    session.close()
    
    return render_template('report.html', customers=customers, sales_totals=sales_totals, popular_items=popular_items)


def get_sales_totals(session):
    today = datetime.date.today()
    start_of_week = today - datetime.timedelta(days=today.weekday())
    start_of_month = today.replace(day=1)
    start_of_year = today.replace(month=1, day=1)

    # Weekly Sales
    weekly_sales = round(session.query(func.sum(Order.total_amount)).filter(
    Order.order_date >= start_of_week
        ).scalar() or 0, 2)


    # Monthly Sales
    monthly_sales = round(session.query(func.sum(Order.total_amount)).filter(
        Order.order_date >= start_of_month
    ).scalar() or 0,2)

    # Yearly Sales
    yearly_sales = round(session.query(func.sum(Order.total_amount)).filter(
        Order.order_date >= start_of_year
    ).scalar() or 0,2)

    return {
        "weekly_sales": weekly_sales,
        "monthly_sales": monthly_sales,
        "yearly_sales": yearly_sales,
    }


def get_most_popular_items(session, limit=5):
    popular_items = (
        session.query(OrderLine.item_id, func.sum(OrderLine.quantity).label('total_quantity'))
        .group_by(OrderLine.item_id)
        .order_by(func.sum(OrderLine.quantity).desc())
        .limit(limit)
        .all()
    )

    # Retrieve item names and details along with quantities
    item_details = []
    for item_id, total_quantity in popular_items:
        item = session.query(Item).filter_by(id=item_id).first()
        item_details.append({"item": item, "total_quantity": total_quantity})

    return item_details
