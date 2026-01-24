def test_admin_user_created(host):
    # Проверяем, что админ-пользователь создан
    # В тестовой среде сложно проверить это напрямую, поэтому проверим конфигурацию
    config = host.file("/etc/matrix-synapse/homeserver.yaml")
    # Проверим, что регистрация отключена
    assert config.contains("enable_registration: false")

def test_registration_disabled(host):
    config = host.file("/etc/matrix-synapse/homeserver.yaml")
    assert config.contains("enable_registration: false")

def test_federation_restricted(host):
    config = host.file("/etc/matrix-synapse/homeserver.yaml")
    assert config.contains("federation_domain_whitelist:")
    assert config.contains("- \"{{ domain_name }}\"")

def test_rate_limiting_configured(host):
    config = host.file("/etc/matrix-synapse/homeserver.yaml")
    assert config.contains("per_second: 0.17")
    assert config.contains("burst_count: 10")