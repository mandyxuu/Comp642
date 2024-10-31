from flask import Blueprint, render_template, request, session as flask_session, redirect, url_for, flash
from models.person import Person,Customer,Staff,CorporateCustomer
from config.db import SessionLocal
import hashlib

auth_bp = Blueprint('auth', __name__)
# Define the root route to redirect to the login page
@auth_bp.route('/')
def home():
    return redirect(url_for('auth.login'))  # Redirect to login page

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Step 1: Input username and password
        username = request.form.get('username')
        password = request.form.get('password')

        # Step 2: Create a new session for database interaction
        session = SessionLocal()
        try:
            # Check if username is provided
            if not username:
                flash('Username is required.', 'danger')
                return redirect(url_for('auth.login'))

            # Check if password is provided
            if not password:
                flash('Password is required.', 'danger')
                return redirect(url_for('auth.login'))

            # Query the database for the user
            user = session.query(Person).filter(Person.username == username).first()
            print(user)
            if not user:
                # If no user found with the username
                flash(f'User with username "{username}" not found.', 'danger')
                return redirect(url_for('auth.login'))

            # Combine password check logic here
            # Hash the entered password and compare with the stored hashed password
            hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()

            if hashed_password != user.password:
                # If the passwords don't match
                flash('Incorrect password.', 'danger')
                return redirect(url_for('auth.login'))

            # If both username and password are correct, log the user in
            flask_session['username'] = user.username
            flask_session['user_id'] = user.id 
            flask_session['type']= user.type # Store the user ID for session tracking
            flash('Login successful!', 'success')
            return redirect(url_for('auth.profile'))  # Use redirect to the profile route

        except Exception as e:
            # Log the error and flash an error message
            print(f"Error during authentication: {e}")
            flash('An error occurred while processing the login request.', 'danger')
            return redirect(url_for('auth.login'))

        finally:
            session.close()  # Close the session after the process is done

    return render_template('login.html')

@auth_bp.route('/profile')
def profile():
    # Check if the user is logged in by checking if 'user_id' is in the session
    if 'user_id' not in flask_session:
        flash('Please log in to view your profile.', 'warning')
        return redirect(url_for('auth.login'))  # Redirect to the login page

    # If the user is logged in, retrieve their information from the database
    user_id = flask_session['user_id']
    session = SessionLocal()
    user = session.query(Person).filter_by(id=user_id).first()

    try:
        if user.type in ['customer', 'corporate_customer']:

            customers = session.query(Person, Customer).join(Customer).filter(Customer.customer_id == user_id).all()
            print(customers)
            for person,customer in customers:
                print(person,customer)
        elif user.type =="staff":
            customers= session.query(Person,Customer).join(Customer).all()

        elif not user:
            flash('User not found.', 'danger')
            return redirect(url_for('auth.login'))

        # Render the profile template and pass the user data
        return render_template('profile.html', user=user,customers = customers)
    finally:
        session.close()  # Ensure the session is closed

@auth_bp.route('/logout')
def logout():
    if 'user_id' not in flask_session:
        flash('You are not logged in.', 'info')
        return redirect(url_for('auth.login'))

    # Clear the session and log the user out
    flask_session.pop('user_id', None)
    flask_session.pop('role', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('auth.login'))

