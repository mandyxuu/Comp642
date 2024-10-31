# test_user.py
from controllers.auth_controller import login

def test_login():
    user = login("test_user", "password")
    assert user is not None
