def test_synapse_package_installed(host):
    pkg = host.package("matrix-synapse")
    assert pkg.is_installed

def test_synapse_service_status(host):
    svc = host.service("matrix-synapse")
    assert svc.is_running
    assert svc.is_enabled

def test_synapse_http_port_open(host):
    # Проверяем, что Synapse слушает на порту 8008
    socket = host.socket("tcp://0.0.0.0:8008")
    assert socket.is_listening

def test_synapse_config_file_exists(host):
    config_file = host.file("/etc/matrix-synapse/homeserver.yaml")
    assert config_file.exists
    assert config_file.is_file