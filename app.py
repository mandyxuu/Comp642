
from flask import Flask
from config import db
import os

def create_app():
    app = Flask(__name__)

    # Load config from db.py
    app.config.from_object(db)

    # Set the secret key for securely signing session data
    app.secret_key = os.urandom(24)  # For development; use a secure key in production

    # Import and register blueprints (controllers)
    from controllers.auth_controller import auth_bp
    from controllers.order_controller import order_bp
    from controllers.veggie_controller import veggie_bp
    from controllers.payment_controller import payment_bp
    from controllers.report_controller import report_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(veggie_bp,url_prefix='/veggie')
    app.register_blueprint(payment_bp)
    app.register_blueprint(report_bp)


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
