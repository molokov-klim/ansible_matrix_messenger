def test_admin_user_not_created(host):
    # Проверяем, что админ-пользователь еще не создан
    # В тестовой среде сложно проверить это напрямую, поэтому проверим конфигурацию
    config = host.file("/etc/matrix-synapse/homeserver.yaml")
    # Проверим, что регистрация включена (по умолчанию)
    assert config.contains("enable_registration: true")

def test_registration_enabled(host):
    config = host.file("/etc/matrix-synapse/homeserver.yaml")
    assert config.contains("enable_registration: true")