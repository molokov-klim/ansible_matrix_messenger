def test_postgres_installed(host):
    pkg = host.package("postgresql")
    assert pkg.is_installed

def test_synapse_database_connection(host):
    config = host.file("/etc/matrix-synapse/homeserver.yaml")
    assert config.contains("database:")
    assert config.contains("psycopg2")
    assert config.contains("matrix_synapse")