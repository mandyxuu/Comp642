
from flask import Blueprint, render_template,redirect,url_for,request,flash,session as flask_session
import datetime
from config.db import SessionLocal
from sqlalchemy.orm import joinedload

from models.person import Person,Customer,Staff,CorporateCustomer
from models.order import Order
from models.orderline import OrderLine
from models.veggie import Item,Veggie,UnitPriceVeggie,PackVeggie,PremadeBox,WeightedVeggie
from models.payment import Payment,CreditCardPayment,DebitCardPayment

order_bp = Blueprint('order', __name__)

# Order list route
@order_bp.route('/list')
def list():
    session = SessionLocal()
    try:
        user_id = flask_session.get('user_id')
        if not user_id:
            flash('You need to log in first.', 'danger')
            return redirect(url_for('auth.login'))

        # Get the user's role
        user = session.query(Person).filter(Person.id == user_id).first()
        flask_session['type'] = user.type
        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('auth.login'))

        # Determine if the user is a customer or staff
        if user.type in ['customer', 'corporate_customer']:
            # Customers can only see their own orders
            orders = (
                session.query(Order, Customer)
                .join(Customer, Order.customer_id == Customer.customer_id)
                .filter(Order.customer_id == user_id)
                .all()
            )



        elif user.type == 'staff':
            # Staff can see all orders
            orders = (
                    session.query(Order, Customer)
                    .join(Customer, Order.customer_id == Customer.customer_id)
                    .all()
                    )
        else:
            flash('Invalid user role.', 'danger')
            return redirect(url_for('auth.login'))
         # Fetch payment information separately
        payments = session.query(Payment).filter(Payment.customer_id == user_id).all()
        # Organize payments by customer_id, with each value as a list of payments
        payment_by_order = {payment.order_id: payment for payment in payments}

        print(payment_by_order)
        # Fetch order items and group by order ID

        order_items = session.query(OrderLine, Item).join(Item, OrderLine.item_id == Item.id).all()
        # Organize items by order_id
        order_items_by_order = {}
        for order_line, item in order_items:

            order_items_by_order.setdefault(order_line.order_id, []).append((order_line, item))

            print(order_line,item)
        print("Before rendering the template")

        return render_template(
            'order.html',
            orders=orders,
            order_items_by_order=order_items_by_order,
            user=user,
            payment_by_order=payment_by_order

        )
     
    except Exception as e:
        flash(f"Failed to retrieve orders: {str(e)}", 'danger')
        print(f"Error details: {str(e)}")  
        return redirect(url_for('veggie.list'))
    finally:
        session.close()

@order_bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'user_id' not in flask_session:
        flash('You need to log in first.', 'danger')
        return redirect(url_for('auth.login'))

    user_id = flask_session['user_id']
    item_id = request.form.get('item_id')
    item_type = request.form.get('item_type')
    quantity = float(request.form.get('quantity'))

    selected_item_ids = request.form.get('selected_item_ids')
    selected_items = selected_item_ids.split(',') if selected_item_ids else []
    
    # Check if quantity is valid
    if quantity <= 0:
        flash('Quantity cannot be zero or less.', 'danger')
        return redirect(url_for('veggie.list'))
    
    # Determine the price based on the item type
    if item_type == "unit_veggie" :
        price = float(request.form.get('price_per_unit'))
    elif item_type == "weighted_veggie":
        price = float(request.form.get('price_per_kilo'))
    elif item_type == "pack_veggie":
        price = float(request.form.get('price_per_pack'))
    elif item_type == "premade_box":
        price = float(request.form.get('box_price'))
    else:
        flash("Invalid item type", "error")
        return redirect(url_for('cart_view'))
     # Check if quantity is valid
    if quantity <= 0:
        flash('Quantity cannot be zero or less.', 'danger')
        return redirect(url_for('veggie.list'))
        

    session = SessionLocal()


    try:
        print(user_id)
        # Create a new order or retrieve the existing pending order for the customer
        order = session.query(Order).filter(Order.customer_id == user_id, Order.order_status == 'pending').first()
        if not order:

            orderDate = datetime.datetime.now()
            print(orderDate)
            order = Order(order_date=orderDate, order_status='pending', customer_id=user_id, total_amount=0.0)
            print(order)
            session.add(order)
            session.commit()  # Commit to get the order ID

            # Deduct the quantity from the appropriate veggie type table
        if item_type == "unit_veggie":
            veggie = session.query(UnitPriceVeggie).filter(UnitPriceVeggie.id == item_id).first()
            if veggie and veggie.quantity >= quantity:
                veggie.quantity -= quantity
            else:
                flash("Insufficient quantity available for this item.", "danger")
                return redirect(url_for('veggie.list'))

        elif item_type == "weighted_veggie":
            veggie = session.query(WeightedVeggie).filter(WeightedVeggie.id == item_id).first()
            if veggie and veggie.weight >= quantity:
                veggie.weight -= quantity
            else:
                flash("Insufficient weight available for this item.", "danger")
                return redirect(url_for('veggie.list'))

        elif item_type == "pack_veggie":
            veggie = session.query(PackVeggie).filter(PackVeggie.id == item_id).first()
            if veggie and veggie.numOfPack >= quantity:
                veggie.numOfPack -= quantity
            else:
                flash("Insufficient packs available for this item.", "danger")
                return redirect(url_for('veggie.list'))

        elif item_type == "premade_box":
            veggie = session.query(PremadeBox).filter(PremadeBox.id == item_id).first()
            if veggie and veggie.num_of_boxes >= quantity:
                veggie.num_of_boxes -= quantity
            else:
                flash("Insufficient boxes available for this item.", "danger")
                return redirect(url_for('veggie.list'))



        # Add item to order

        total_price = quantity * price
        if flask_session['type'] == "corporate_customer":
            total_price = total_price *0.9

        # Prepare the order line with selected items if it's a premade box
        if item_type == "premade_box":
            # Create the OrderLine with selected item IDs for a premade box
            order_line = OrderLine(
                order_id=order.order_id,
                item_id=item_id,
                item_type=item_type,
                quantity=quantity,
                price=price,
                total_price=total_price,
                selected_item_1=int(selected_items[0]) if len(selected_items) > 0 else None,
                selected_item_2=int(selected_items[1]) if len(selected_items) > 1 else None,
                selected_item_3=int(selected_items[2]) if len(selected_items) > 2 else None,
                selected_item_4=int(selected_items[3]) if len(selected_items) > 3 else None
            )
        else:
            # Create a regular OrderLine for other item types
            order_line = OrderLine(
                order_id=order.order_id,
                item_id=item_id,
                item_type=item_type,
                quantity=quantity,
                price=price,
                total_price=total_price
            )

        session.add(order_line)
        
        # Update the total amount in the order
        order.total_amount += order_line.total_price
        
        session.commit()
        flash('Item added to cart successfully!', 'success')
        return redirect(url_for('veggie.list'))

    except Exception as e:
        session.rollback()
        flash(f'Failed to add item to cart: {str(e)}', 'danger')
        return redirect(url_for('veggie.list'))

    finally:
        session.close()

@order_bp.route('/cancel_item/<int:order_line_id>', methods=['POST'])
def cancel_item(order_line_id):
    session = SessionLocal()

    try:
        order_line = (
            session.query(OrderLine)
            .options(joinedload(OrderLine.order))  # Eager load the associated Order

            .filter(OrderLine.orderline_id == order_line_id).first()
        )
        if order_line and order_line.order.order_status == 'pending':
            order = session.query(Order).filter(Order.order_id==order_line.order_id).first()
           

            # Recover the quantity for the specific item based on its type
            if order_line.item_type == "unit_veggie":
                veggie = session.query(UnitPriceVeggie).filter(UnitPriceVeggie.id == order_line.item_id).first()
                if veggie:
                    veggie.quantity += order_line.quantity

            elif order_line.item_type == "weighted_veggie":
                veggie = session.query(WeightedVeggie).filter(WeightedVeggie.id == order_line.item_id).first()
                if veggie:
                    veggie.weight += order_line.quantity

            elif order_line.item_type == "pack_veggie":
                veggie = session.query(PackVeggie).filter(PackVeggie.id == order_line.item_id).first()
                if veggie:
                    veggie.numOfPack += order_line.quantity

            elif order_line.item_type == "premade_box":
                veggie = session.query(PremadeBox).filter(PremadeBox.id == order_line.item_id).first()
                if veggie:
                    veggie.num_of_boxes += order_line.quantity


            # Check if the order only has this one item left
            order_items_count = session.query(OrderLine).filter(OrderLine.order_id == order.order_id).count()
            if order_items_count == 1:
                # If only one item, cancel the entire order
                order.order_status = 'canceled'
                order.total_amount = 0  # Reset total amount to 0
            else:
                # Just deduct the item's total price from the order's total amount
                order.total_amount-= order_line.total_price


            # Optionally: Implement any business logic for cancellation here

            session.delete(order_line)
            session.commit()

            flash('Item successfully canceled.', 'success')
        else:
            flash('Item not found or cannot be canceled.', 'danger')
    except Exception as e:
        session.rollback()
        flash('An error occurred while canceling the item.'+ str(e), 'danger')
        print(str(e))
    finally:
        session.close()
    return redirect(url_for('order.list'))  # Redirect to your order list page

@order_bp.route('/cancel_order/<int:order_id>', methods=['POST'])
def cancel_order(order_id):
    session = SessionLocal()
    try:
        
        order = session.query(Order).filter(Order.order_id == order_id).first()
        if order and order.order_status == 'pending':
            # Optionally: Implement any business logic for cancellation here
                        # Restore quantities for each item in the order based on item type
            order_lines = session.query(OrderLine).filter(OrderLine.order_id == order_id).all()
            
            # Recover the quantities for each item in the order
            for order_line in order_lines:
                if order_line.item_type == "unit_veggie":
                    veggie = session.query(UnitPriceVeggie).filter(UnitPriceVeggie.id == order_line.item_id).first()
                    if veggie:
                        veggie.quantity += order_line.quantity

                elif order_line.item_type == "weighted_veggie":
                    veggie = session.query(WeightedVeggie).filter(WeightedVeggie.id == order_line.item_id).first()
                    if veggie:
                        veggie.weight += order_line.quantity

                elif order_line.item_type == "pack_veggie":
                    veggie = session.query(PackVeggie).filter(PackVeggie.id == order_line.item_id).first()
                    if veggie:
                        veggie.numOfPack += order_line.quantity

                elif order_line.item_type == "premade_box":
                    veggie = session.query(PremadeBox).filter(PremadeBox.id == order_line.item_id).first()
                    if veggie:
                        veggie.num_of_boxes += order_line.quantity
# Update the order status to 'canceled'
            order.order_status = 'canceled'
            session.commit()
            flash('Order successfully canceled.', 'success')
        else:
            flash('Order not found or cannot be canceled.', 'danger')
    except Exception as e:
        session.rollback()
        flash('An error occurred while canceling the order.', 'danger')
        print(str(e))
    finally:
        session.close()
    return redirect(url_for('order.list'))  # Redirect to your order list page

