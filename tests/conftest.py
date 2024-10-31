import pytest
from config.db import Base, SessionLocal, engine
from app import create_app  # Adjust if your app factory is located elsewhere

@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",  # In-memory database for testing
        "SECRET_KEY": "testsecretkey"  # Set a secret key for sessions
    })
    return app

@pytest.fixture(scope="session")
def db(app):
    # Set up the database schema within the app context
    with app.app_context():
        Base.metadata.create_all(bind=engine)
    yield
    # Teardown: Drop all tables after the test session
    with app.app_context():
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def session(db):
    # Use a new SQLAlchemy session for each test
    session = SessionLocal()
    yield session
    session.rollback()  # Rollback any changes after each test
    session.close()

@pytest.fixture(scope="function")
def client(app):
    # Use Flask’s test client for HTTP requests
    return app.test_client()
