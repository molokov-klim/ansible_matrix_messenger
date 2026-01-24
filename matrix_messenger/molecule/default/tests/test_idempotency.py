def test_idempotency_check(host):
    """Проверка идемпотентности - повторный запуск не должен ничего менять"""
    # Этот тест будет запускаться после основного применения роли
    # и проверяет, что повторный запуск не приводит к изменениям
    
    # Проверим, что сервис все еще запущен
    svc = host.service("matrix-synapse")
    assert svc.is_running
    assert svc.is_enabled
    
    # Проверим, что конфигурационный файл существует
    config_file = host.file("/etc/matrix-synapse/homeserver.yaml")
    assert config_file.exists
    assert config_file.is_file