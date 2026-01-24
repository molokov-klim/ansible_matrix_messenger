import pytest

def test_nginx_installed(host):
    # Пропускаем в CI - nginx не устанавливается в Docker
    if host.ansible.get_variables().get('molecule_test'):
        pytest.skip("Nginx не устанавливается в тестовом окружении Docker")
    
    pkg = host.package("nginx")
    assert pkg.is_installed

def test_ssl_certificate_exists(host):
    # Пропускаем в CI - SSL сертификаты требуют реальный домен
    if host.ansible.get_variables().get('molecule_test'):
        pytest.skip("SSL сертификаты не получаются в тестовом окружении Docker")
        
    domain = host.ansible.get_variables()['domain_name']
    cert_path = f"/etc/letsencrypt/live/{domain}/fullchain.pem"
    assert host.file(cert_path).exists

def test_nginx_matrix_site_enabled(host):
    if host.ansible.get_variables().get('molecule_test'):
        pytest.skip("Nginx не устанавливается в тестовом окружении Docker")
        
    assert host.file("/etc/nginx/sites-enabled/matrix").exists

def test_nginx_running_and_enabled(host):
    if host.ansible.get_variables().get('molecule_test'):
        pytest.skip("Nginx не устанавливается в тестовом окружении Docker")
        
    nginx = host.service("nginx")
    assert nginx.is_running
    assert nginx.is_enabled

def test_https_port_open(host):
    if host.ansible.get_variables().get('molecule_test'):
        pytest.skip("HTTPS порт не открыт в тестовом окружении Docker")
        
    # Проверяем, что Nginx слушает на порту 443
    socket = host.socket("tcp://0.0.0.0:443")
    assert socket.is_listening

def test_http_redirect_to_https(host):
    if host.ansible.get_variables().get('molecule_test'):
        pytest.skip("HTTP редирект не настроен в тестовом окружении Docker")
        
    # Проверяем, что HTTP запросы перенаправляются на HTTPS
    cmd = host.run("curl -I http://localhost")
    assert "301 Moved Permanently" in cmd.stdout or "302 Found" in cmd.stdout
    assert "Location: https://" in cmd.stdout