from models.person import Customer
from models.order import Order
from flask import Blueprint, render_template,redirect,url_for,request,flash,session as flask_session
from datetime import datetime
def test_list_orders_customer_view(client, session):
    customer = Customer(username="testcustomer", password="password", type="customer")
    session.add(customer)
    session.commit()
    flask_session["user_id"] = customer.id
    flask_session["user_type"] = customer.type
    
    response = client.get("/order/list")
    assert response.status_code == 200
    assert b"Orders" in response.data

def test_add_to_cart(client, session):
    customer = Customer(username="customer", password="password", type="customer")
    session.add(customer)
    session.commit()
    
    response = client.post("/add_to_cart", data={
        "item_id": 1,
        "item_type": "unit_veggie",
        "quantity": 1,
        "price_per_unit": 2.0,
    })
    assert b"Item added to cart successfully!" in response.data

def test_cancel_item(client, session):
    order = Order(order_date=datetime.now(), order_status="pending", customer_id=1)
    session.add(order)
    session.commit()
    
    response = client.post(f"/cancel_item/{order.id}")
    assert b"Item successfully canceled." in response.data
