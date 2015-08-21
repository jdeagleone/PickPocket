from app.auth_module.views import authenticate


def test_authenticate():
    assert authenticate()
