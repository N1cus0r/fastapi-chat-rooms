from faker import Faker
from factory.mogo import MogoFactory

from src.auth.models import User

fake = Faker()


class UserFactory(MogoFactory):
    class Meta:
        model = User

    username = fake.name()
    email = fake.email()
    hashed_password = fake.password()
