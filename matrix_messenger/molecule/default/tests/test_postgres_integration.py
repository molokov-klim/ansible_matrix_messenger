def test_postgres_not_installed(host):
    assert not host.package("postgresql").is_installed

def test_synapse_database_connection(host):
    config = host.file("/etc/matrix-synapse/homeserver.yaml")
    assert not config.contains("database:")
    assert not config.contains("postgres://")