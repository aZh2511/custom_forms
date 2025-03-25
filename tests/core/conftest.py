import pytest
from tests.mocks.core.domain.repositories import TestsRepository


@pytest.fixture()
def repository() -> TestsRepository:
    return TestsRepository()
