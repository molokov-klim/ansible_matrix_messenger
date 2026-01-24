def test_hosts_file(host):
    f = host.file('/etc/hosts')
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'

def test_apt_cache_updated(host):
    # Проверяем что apt может обновить кэш без ошибок
    cmd = host.run("apt-get update")
    assert cmd.rc == 0, "Не удалось обновить apt кэш"