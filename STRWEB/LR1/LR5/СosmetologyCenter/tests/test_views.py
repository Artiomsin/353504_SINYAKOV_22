from django.urls import reverse
import pytest

@pytest.mark.django_db
def test_home_view(client):
    response = client.get(reverse('home'))
    assert response.status_code == 200
    assert 'latest_news' in response.context

@pytest.mark.django_db
def test_service_list_view(client, service):
    response = client.get(reverse('services'))
    assert response.status_code == 200
    assert service in response.context['services']

@pytest.mark.parametrize("url_name, expected_status", [
    ('about', 200),
    ('privacy-policy', 200),
])
def test_static_views(client, url_name, expected_status):
    response = client.get(reverse(url_name))
    assert response.status_code == expected_status

@pytest.mark.django_db
def test_doctor_detail_view(client, doctor_user):
    response = client.get(reverse('doctor-detail', kwargs={'pk': doctor_user.pk}))
    assert response.status_code == 200
    assert response.context['doctor'] == doctor_user

@pytest.mark.django_db
def test_signup_view(client):
    response = client.get(reverse('signup'))
    assert response.status_code == 200
    assert 'form' in response.context