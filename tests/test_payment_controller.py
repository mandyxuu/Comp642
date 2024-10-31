from datetime import datetime
from models.payment import CreditCardPayment
from models.person import Customer

def test_process_credit_payment(client, session):
    customer = Customer(username="corpuser", password="password", type="corporate_customer")
    session.add(customer)
    session.commit()
    
    response = client.post("/process", data={
        "payment_type": "credit",
        "card_number": "1234567812345678",
        "card_holder": "Test User",
        "expiry_date": "12/24",
        "cvv": "123",
        "amount": 100.0,
        "user_id": customer.id,
    })
    assert b"Payment of" in response.data
