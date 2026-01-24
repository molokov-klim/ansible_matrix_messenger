import os

def test_readme_exists():
    assert os.path.exists("README.md"), "README.md не найден"

def test_readme_contains_required_sections():
    with open("README.md", "r") as f:
        content = f.read()

    required_sections = [
        "# Matrix Messenger Ansible Role",
        "## Описание",
        "## Требования",
        "## Переменные",
        "## Пример использования",
        "## Установка",
        "## Безопасность"
    ]

    for section in required_sections:
        assert section in content, f"Отсутствует раздел: {section}"

def test_contributing_exists():
    assert os.path.exists("CONTRIBUTING.md"), "CONTRIBUTING.md не найден"

def test_examples_exist():
    assert os.path.exists("examples/staging.inventory.ini"), "Пример inventory для staging не найден"
    assert os.path.exists("examples/production.inventory.ini"), "Пример inventory для production не найден"
    assert os.path.exists("examples/env_staging.example"), "Пример .env для staging не найден"
    assert os.path.exists("examples/env_production.example"), "Пример .env для production не найден"