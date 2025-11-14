import pytest
from .factories import ClientFactory, DoctorFactory, ServiceFactory
from core.models import Appointment

@pytest.fixture
def client_user(db):
    user = ClientFactory()
    return user.client

@pytest.fixture
def doctor_user(db):
    return DoctorFactory()

@pytest.fixture
def service(db):
    return ServiceFactory()

@pytest.fixture
def appointment(db, client_user, doctor_user, service):
    return Appointment.objects.create(
        client=client_user,
        doctor=doctor_user.doctor,
        service=service,
        date_time='2024-01-01 10:00'
    )