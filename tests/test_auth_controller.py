import hashlib
from models.person import Person

def test_login_success(client, session):
    hashed_password = hashlib.sha256("password".encode()).hexdigest()
    # Ensure all fields required by `Person` are provided
    session.add(Person(
        first_name="Test",
        last_name="User",
        username="testuser",
        password=hashed_password,
        type="customer"
    ))
    session.commit()
    
    # Attempt login
    response = client.post("/login", data={"username": "testuser", "password": "password"})
    print(response.data)  # Debug line to inspect login response
    
    # Assertions
    assert response.status_code == 302
    with client.session_transaction() as sess:
        # Check if the login was successful by looking for 'username' in session
        assert "username" in sess
        assert sess["username"] == "testuser"


def test_login_invalid_credentials(client):
    response = client.post("/login", data={"username": "wronguser", "password": "wrongpass"})
    print(response.data)  # Debug line to inspect error message in the response
    
    # Adjust assertion based on actual error message in your app
    assert b"An error occurred while processing the login request." in response.data  # Adjust this as necessary


def test_logout(client):
    client.post("/login", data={"username": "testuser", "password": "password"})
    client.get("/logout")
    
    with client.session_transaction() as sess:
        assert "username" not in sess
