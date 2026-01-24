def test_ubuntu_system(host):
    # Проверяем, что система Ubuntu
    assert host.system_info.distribution == "ubuntu"

def test_systemd_running(host):
    # Проверяем что systemd работает
    systemd = host.service("systemd")
    assert systemd.is_running