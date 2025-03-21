from core.domain.models import Test


def test_dummy() -> None:
    test = Test('ok?')

    assert test.a == 'ok?'


def test_fail():
    assert 1 == 2
