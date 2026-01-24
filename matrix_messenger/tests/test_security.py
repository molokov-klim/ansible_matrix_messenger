import os

def test_no_secrets_in_git(host):
    """Проверка, что секреты не попали в git"""
    # Ищем пароли и ключи в закоммиченных файлах
    sensitive_patterns = [
        "ANSIBLE_PASSWORD",
        "MATRIX_ADMIN_PASSWORD",
        "POSTGRES_PASSWORD",
        "ssh-rsa",
        "-----BEGIN"
    ]

    for pattern in sensitive_patterns:
        cmd = host.run(f"git grep -i '{pattern}' -- ':!tests' ':!scripts' 2>/dev/null || true")
        assert cmd.stdout.strip() == "", f"Найден секрет в git: {pattern}"

def test_required_env_vars(host):
    """Проверка наличия обязательных переменных окружения"""
    required_vars = [
        "ANSIBLE_HOST",
        "ANSIBLE_USER",
        "ANSIBLE_PASSWORD",
        "MATRIX_ADMIN_PASSWORD",
        "POSTGRES_PASSWORD"
    ]

    for var in required_vars:
        assert os.getenv(var) is not None, f"Отсутствует обязательная переменная: {var}"