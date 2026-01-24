def test_hosts_file(host):
    f = host.file('/etc/hosts')
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'

def test_can_run_commands(host):
    # Проверяем что можем выполнять команды
    cmd = host.run("echo 'test'")
    assert cmd.rc == 0
    assert cmd.stdout.strip() == 'test'