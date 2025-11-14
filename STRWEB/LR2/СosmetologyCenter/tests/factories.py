import factory
from django.contrib.auth.models import User
from core.models import Client, Doctor, Service, Appointment, Review, Cabinet

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f'user{n}')
    email = factory.LazyAttribute(lambda o: f'{o.username}@example.com')
    password = factory.PostGenerationMethodCall('set_password', 'password')

class ClientFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Client

    user = factory.SubFactory(UserFactory)
    phone = "+375 (29) 123-45-67"
    birth_date = factory.Faker('date_object')
    address = factory.Faker('address')

class CabinetFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cabinet
    
    name = factory.Faker('word')

class DoctorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Doctor

    cabinet = factory.SubFactory(CabinetFactory)
    experience = factory.Faker('pyint', min_value=1, max_value=40)
    user = factory.SubFactory(UserFactory)
    full_name = factory.Faker('name')
    license_number = factory.Sequence(lambda n: f'LIC-{n}')
    phone = "+375 (29) 765-43-21"
    email = factory.LazyAttribute(lambda o: f'{o.user.username}@clinic.com')

class ServiceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Service

    name = factory.Sequence(lambda n: f'Service {n}')
    price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    duration = factory.Faker('time_delta', end_datetime=None)