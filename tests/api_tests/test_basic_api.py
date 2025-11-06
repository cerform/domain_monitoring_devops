# tests/api_tests/test_basic_api.py
import pytest

def test_addition():
    """Простой тест для проверки pytest"""
    assert 2 + 3 == 5

@pytest.mark.parametrize("a,b,result", [(1, 1, 2), (3, 2, 5), (-1, 1, 0)])
def test_parametrized(a, b, result):
    """Параметризованный тест"""
    assert a + b == result

def test_uppercase():
    """Проверка строк"""
    s = "jenkins"
    assert s.upper() == "JENKINS"
