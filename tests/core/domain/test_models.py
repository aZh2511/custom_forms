from core.domain.models import Test
import pytest


def test_dummy() -> None:
    test = Test('ok?')

    assert test.a == 'ok?'


@pytest.mark.xfail
def test_fail():
    assert 1 == 2
