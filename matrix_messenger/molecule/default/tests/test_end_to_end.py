import requests
import json

def test_matrix_api_health(host):
    domain = host.ansible.get_variables()['domain_name']

    # Проверка доступности API
    response = requests.get(f"https://{domain}/_matrix/client/versions", verify=False)
    assert response.status_code == 200
    assert "versions" in response.json()

def test_user_login(host):
    domain = host.ansible.get_variables()['domain_name']
    admin_user = host.ansible.get_variables().get('admin_username', 'admin')
    admin_pass = host.ansible.get_variables().get('matrix_admin_password', 'default_admin_password')

    payload = {
        "type": "m.login.password",
        "user": admin_user,
        "password": admin_pass
    }

    response = requests.post(
        f"https://{domain}/_matrix/client/r0/login",
        data=json.dumps(payload),
        headers={"Content-Type": "application/json"},
        verify=False
    )

    assert response.status_code == 200
    assert "access_token" in response.json()

def test_synapse_running(host):
    # Проверяем, что Synapse запущен
    svc = host.service("matrix-synapse")
    assert svc.is_running
    assert svc.is_enabled

def test_nginx_running(host):
    # Проверяем, что Nginx запущен
    svc = host.service("nginx")
    assert svc.is_running
    assert svc.is_enabled

def test_postgres_running(host):
    # Проверяем, что PostgreSQL запущен
    svc = host.service("postgresql")
    assert svc.is_running
    assert svc.is_enabled

def test_https_port_open(host):
    # Проверяем, что HTTPS порт открыт
    socket = host.socket("tcp://0.0.0.0:443")
    assert socket.is_listening

def test_http_redirect_to_https(host):
    # Проверяем, что HTTP запросы перенаправляются на HTTPS
    cmd = host.run("curl -I http://localhost")
    assert "301 Moved Permanently" in cmd.stdout or "302 Found" in cmd.stdout
    assert "Location: https://" in cmd.stdout