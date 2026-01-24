import requests
import json

def test_matrix_api_health_after_deployment(host):
    domain = host.ansible.get_variables()['domain_name']

    # Проверка доступности API
    response = requests.get(f"https://{domain}/_matrix/client/versions", verify=False)
    assert response.status_code == 200
    assert "versions" in response.json()

def test_monitoring_services_running(host):
    # Проверяем, что сервисы мониторинга запущены
    node_exporter = host.service("prometheus-node-exporter")
    assert node_exporter.is_running
    assert node_exporter.is_enabled

    fail2ban = host.service("fail2ban")
    assert fail2ban.is_running
    assert fail2ban.is_enabled

def test_backup_scripts_exist(host):
    # Проверяем, что скрипты резервного копирования существуют
    backup_db_script = host.file("/usr/local/bin/backup_matrix_db.sh")
    assert backup_db_script.exists
    assert backup_db_script.is_file

    backup_config_script = host.file("/usr/local/bin/backup_matrix_config.sh")
    assert backup_config_script.exists
    assert backup_config_script.is_file

def test_backup_directories_exist(host):
    # Проверяем, что директории для резервных копий существуют
    backup_dir = host.file("/var/backups/matrix")
    assert backup_dir.exists
    assert backup_dir.is_directory