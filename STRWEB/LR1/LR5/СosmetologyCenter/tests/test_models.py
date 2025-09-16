import pytest
from django.core.exceptions import ValidationError
from core.models import Client, Doctor, Service
from .factories import ClientFactory, DoctorFactory, ServiceFactory
import datetime

@pytest.mark.django_db
def test_client_age_validation():
    client = ClientFactory.build(birth_date=datetime.date.today() - datetime.timedelta(days=365*17))
    with pytest.raises(ValidationError):
        client.full_clean()

@pytest.mark.django_db
def test_doctor_group_assignment():
    doctor = DoctorFactory()
    assert doctor.user.groups.filter(name='Doctors').exists()

@pytest.mark.django_db
def test_service_duration_formatting():
    service = ServiceFactory(duration=datetime.timedelta(hours=1, minutes=30))
    assert service.duration_formatted() == "01:30"