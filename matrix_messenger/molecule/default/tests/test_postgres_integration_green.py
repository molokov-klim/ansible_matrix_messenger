import pytest

def test_postgres_installed(host):
    pytest.skip("Installation tests disabled in minimal converge mode")

def test_synapse_database_connection(host):
    pytest.skip("Installation tests disabled in minimal converge mode")