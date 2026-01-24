def test_hosts_file(host):
    f = host.file('/etc/hosts')
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'

def test_apt_update(host):
    cmd = host.run("apt list --upgradable 2>/dev/null | grep -v 'Listing...' | wc -l")
    assert int(cmd.stdout.strip()) == 0, "Есть обновления пакетов"