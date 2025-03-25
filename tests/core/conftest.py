import pytest
from tests.mocks.core.domain.repositories import TestsRepository
from faker import Faker


@pytest.fixture
def faker() -> Faker:
    return Faker()


@pytest.fixture()
def repository() -> TestsRepository:
    return TestsRepository()
