import os

def test_required_environment_variables():
    required_vars = [
        'ANSIBLE_HOST',
        'ANSIBLE_USER', 
        'ANSIBLE_PASSWORD',
        'MATRIX_ADMIN_PASSWORD',
        'POSTGRES_PASSWORD'
    ]
    
    for var in required_vars:
        assert var in os.environ, f"Переменная окружения {var} не установлена"

def test_sensitive_data_not_in_defaults():
    # Проверяем, что чувствительные данные не хранятся в defaults
    with open('defaults/main.yml', 'r') as f:
        content = f.read()
        sensitive_patterns = ['password', 'secret', 'token']
        for pattern in sensitive_patterns:
            assert pattern.lower() not in content.lower(), f"Найден потенциальный секрет в defaults: {pattern}"