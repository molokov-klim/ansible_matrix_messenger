def test_ubuntu_system(host):
    # Проверяем, что система Ubuntu
    assert host.system_info.distribution == "ubuntu"
    
def test_python_available(host):
    # Проверяем что Python доступен
    cmd = host.run("python3 --version")
    assert cmd.rc == 0
    assert "Python 3" in cmd.stdout or "Python 3" in cmd.stderr