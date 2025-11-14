import pytest
from core.forms import ClientSignUpForm, ReviewForm

@pytest.mark.parametrize("phone, valid", [
    ("+375 (29) 123-45-67", True),
    ("+375(29)123-45-67", False),
    ("12345", False),
    ("+375 (44) 987-65-43", True),
])
@pytest.mark.django_db
def test_client_signup_phone_validation(phone, valid):
    form_data = {
        'first_name': 'Test',
        'last_name': 'User',
        'username': 'testuser',
        'email': 'test@example.com',
        'password1': 'Testpass123',
        'password2': 'Testpass123',
        'phone': phone,
        'birth_date': '2000-01-01',
        'address': 'Test Address'
    }
    form = ClientSignUpForm(data=form_data)
    assert form.is_valid() == valid
    if not valid:
        assert 'phone' in form.errors

@pytest.mark.django_db
def test_review_form_validation():
    form_data = {'rating': 5, 'text': 'Great service!'}
    form = ReviewForm(data=form_data)
    assert form.is_valid()