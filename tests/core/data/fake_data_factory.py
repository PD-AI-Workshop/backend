from faker import Faker
from datetime import datetime


class FakeDataFactory:
    def __init__(self, faker: Faker):
        self.__faker = faker

    def integer(self, start: int = 1, end: int = 30, step: int = 1) -> int:
        return self.__faker.random_int(min=start, max=end, step=step)

    def time_reading(self) -> int:
        return self.integer(start=1, end=100)

    def email(self) -> str:
        return self.__faker.email()

    def username(self) -> str:
        return self.__faker.user_name()

    def password(self) -> str:
        return self.__faker.password()

    def datetime(self) -> datetime:
        return datetime.now()

    def ID(self) -> int:
        return self.integer(start=1, end=999)

    def title(self) -> str:
        return self.__faker.word()

    def list_with_ids(self, length: int = 3) -> list[int]:
        return [self.integer(start=1, end=100) for i in range(length)]

    def url(self) -> str:
        return self.__faker.url()


fake_data_factory = FakeDataFactory(faker=Faker())
