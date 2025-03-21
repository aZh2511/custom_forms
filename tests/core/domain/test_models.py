from core.domain.models import Test
from pytest import xfail


def test_dummy() -> None:
    test = Test('ok?')

    assert test.a == 'ok?'


@xfail
def test_fail():
    assert 1 == 2
