from flask import Blueprint, render_template, request, flash, redirect, url_for,session as flask_session
from datetime import datetime
from config.db import SessionLocal
from models.payment import Payment,CreditCardPayment, DebitCardPayment
from models.order import Order,OrderLine
from models.person import Person,Customer,CorporateCustomer

payment_bp = Blueprint('payment', __name__)

# Payment process route
@payment_bp.route('/process', methods=['GET', 'POST'])
def process():
    if request.method == 'POST':
        payment_type = request.form.get('payment_type')
        card_number = request.form.get('card_number')
        card_holder = request.form.get('card_holder')
        expiry_date = request.form.get('expiry_date')
        cvv = request.form.get('cvv')
        amount = request.form.get('amount')
        amount = float(amount)
        bank_name = request.form.get('bank_name')  # Only for debit card payments
        order_id = request.form.get('order_id')  # Get order_id from the form
        customer_id = request.form.get('user_id')  # Get order_id from the form
        is_delivery = request.form.get('delivery_option', 'false').lower() == 'true'
        
        session = SessionLocal()

        # If user is staff, find the customer_id based on order_id
        if flask_session['type'] == 'staff':
            # Query to find the customer_id based on order_id
                order = session.query(Order).filter(Order.order_id == order_id).first()
                if order:
                    customer_id = order.customer_id  # Override customer_id from form



        try:
           
                 
            # Add delivery charge if delivery is selected and the order weight is over 20 kg
            if is_delivery:
                amount += 10.0
            
            # Simulate the current date as the payment date
            payment_date = datetime.now()

            # Begin processing based on payment type
            if payment_type == 'account_balance':
                    # Handle payment with account balance
                    customer = session.query(Customer).filter(Customer.id == customer_id).first()
                    
                    if customer and customer.cust_balance <= customer.max_owing:
                        # Deduct the amount from the account balance
                        customer.cust_balance += amount
                        
                        # Create a record of the balance payment (optional)
                        new_payment = Payment(
                            payment_amount=amount,
                            payment_date=payment_date,
                            customer_id=customer_id,
                            order_id=order_id,
                            is_delivery = is_delivery

                        )


            # Process credit card payment
            elif payment_type == 'credit':
                # Create a new CreditCardPayment object
                new_payment = CreditCardPayment(
                    payment_amount=float(amount),
                    payment_date=payment_date,
                    customer_id=customer_id,
                    order_id=order_id,
                    card_expiry_date=expiry_date,
                    card_number=card_number,
                    card_type='credit',
                    is_delivery = is_delivery

                )

            # Process debit card payment
            elif payment_type == 'debit':
                # Create a new DebitCardPayment object
                new_payment = DebitCardPayment(
                    payment_amount=float(amount),
                    payment_date=payment_date,
                    customer_id=customer_id,
                    order_id=order_id,
                    bank_name=bank_name,
                    debit_card_number=card_number,
                    is_delivery = is_delivery

                )

            # Add the new payment to the session and commit
            session.add(new_payment)
            session.commit()
            # Update the order status to "paid"
            order = session.query(Order).filter(Order.order_id == order_id).first()
            if order:
                order.order_status = 'paid'
                session.commit()

            flash(f'Payment of ${amount} has been processed successfully!', 'success')
            return redirect(url_for('payment.process'))

        except Exception as e:
            session.rollback()
            flash(f'Failed to process payment: {str(e)}', 'danger')

        finally:
            session.close()

    return redirect(url_for('order.list'))

