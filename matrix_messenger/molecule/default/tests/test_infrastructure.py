def test_molecule_infrastructure(host):
    # Этот тест должен упасть, потому что роль еще не создана
    assert host.package("nonexistent-package").is_installed