import os
import pathlib

# Определяем путь к корню роли (matrix_messenger/)
ROLE_ROOT = pathlib.Path(__file__).parent.parent.parent.resolve()

def test_readme_exists():
    # Проверяем, что файл README.md существует в корне роли
    readme_path = ROLE_ROOT / "README.md"
    assert readme_path.exists(), f"README.md не найден: {readme_path}"

def test_readme_contains_required_sections():
    readme_path = ROLE_ROOT / "README.md"
    with open(readme_path, "r", encoding='utf-8') as f:
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
    # Проверяем, что файл CONTRIBUTING.md существует
    contributing_path = ROLE_ROOT / "CONTRIBUTING.md"
    assert contributing_path.exists(), f"CONTRIBUTING.md не найден: {contributing_path}"

def test_examples_exist():
    # Проверяем, что примеры существуют в директории examples/
    examples_dir = ROLE_ROOT / "examples"
    
    required_examples = [
        "staging.inventory.ini",
        "production.inventory.ini",
        "env_staging.example",
        "env_production.example"
    ]
    
    for example in required_examples:
        example_path = examples_dir / example
        assert example_path.exists(), f"Пример не найден: {example_path}"

def test_quickstart_exists():
    # Проверяем новый файл QUICKSTART.md
    quickstart_path = ROLE_ROOT / "QUICKSTART.md"
    assert quickstart_path.exists(), f"QUICKSTART.md не найден: {quickstart_path}"

def test_env_example_exists():
    # Проверяем наличие env.example
    env_example_path = ROLE_ROOT / "env.example"
    assert env_example_path.exists(), f"env.example не найден: {env_example_path}"

def test_inventory_example_exists():
    # Проверяем наличие inventory.ini.example
    inventory_example_path = ROLE_ROOT / "inventory.ini.example"
    assert inventory_example_path.exists(), f"inventory.ini.example не найден: {inventory_example_path}"