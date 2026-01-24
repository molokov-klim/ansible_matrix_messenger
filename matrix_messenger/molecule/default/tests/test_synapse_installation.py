def test_synapse_package_installed(host):
    assert not host.package("matrix-synapse").is_installed, "Пакет установлен до реализации"

def test_synapse_service_status(host):
    assert not host.service("matrix-synapse").is_running, "Сервис запущен до реализации"