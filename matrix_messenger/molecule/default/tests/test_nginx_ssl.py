def test_nginx_not_installed(host):
    assert not host.package("nginx").is_installed

def test_ssl_certificate_missing(host):
    cert_path = f"/etc/letsencrypt/live/{host.ansible.get_variables()['domain_name']}/fullchain.pem"
    assert not host.file(cert_path).exists