import pytest

def test_idempotency_check(host):
    """Проверка идемпотентности - повторный запуск не должен ничего менять"""
    pytest.skip("Installation tests disabled in minimal converge mode")