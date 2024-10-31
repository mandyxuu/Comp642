from datetime import datetime
from models.order import Order

def test_sales_report(client, session):
    session.add(Order(total_amount=200.0, order_date=datetime.now()))
    session.commit()
    
    response = client.get("/report")
    assert response.status_code == 200
    assert b"Sales Totals" in response.data
