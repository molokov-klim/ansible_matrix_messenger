import os
import pathlib

# Определяем путь к корню роли (ansible_matrix_messenger/)
# __file__ = .../matrix_messenger/molecule/default/tests/test_documentation.py
# parent.parent.parent.parent = .../ansible_matrix_messenger/
ROLE_ROOT = pathlib.Path(__file__).parent.parent.parent.parent.resolve()

# Логгирование переменной ROLE_ROOT
print(f"DEBUG: ROLE_ROOT = {ROLE_ROOT}")

def test_readme_exists():
    # Проверяем, что файл README.md существует в корне роли
    readme_path = ROLE_ROOT / "README.md"
    print(f"DEBUG: readme_path = {readme_path}")
    assert readme_path.exists(), f"README.md не найден: {readme_path}"

def test_readme_contains_required_sections():
    readme_path = ROLE_ROOT / "README.md"
    print(f"DEBUG: readme_path = {readme_path}")
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
        print(f"DEBUG: Проверяем наличие раздела: {section}")
        assert section in content, f"Отсутствует раздел: {section}"

def test_contributing_exists():
    # Проверяем, что файл CONTRIBUTING.md существует
    contributing_path = ROLE_ROOT / "CONTRIBUTING.md"
    print(f"DEBUG: contributing_path = {contributing_path}")
    assert contributing_path.exists(), f"CONTRIBUTING.md не найден: {contributing_path}"

def test_examples_exist():
    # Проверяем, что примеры существуют в директории examples/
    examples_dir = ROLE_ROOT / "examples"
    print(f"DEBUG: examples_dir = {examples_dir}")

    required_examples = [
        "staging.inventory.ini",
        "production.inventory.ini",
        "env_staging.example",
        "env_production.example"
    ]

    for example in required_examples:
        example_path = examples_dir / example
        print(f"DEBUG: example_path = {example_path}")
        assert example_path.exists(), f"Пример не найден: {example_path}"

def test_quickstart_exists():
    # Проверяем новый файл QUICKSTART.md
    quickstart_path = ROLE_ROOT / "QUICKSTART.md"
    print(f"DEBUG: quickstart_path = {quickstart_path}")
    assert quickstart_path.exists(), f"QUICKSTART.md не найден: {quickstart_path}"

def test_env_example_exists():
    # Проверяем наличие env.example
    env_example_path = ROLE_ROOT / "env.example"
    print(f"DEBUG: env_example_path = {env_example_path}")
    assert env_example_path.exists(), f"env.example не найден: {env_example_path}"

def test_inventory_example_exists():
    # Проверяем наличие inventory.ini.example
    inventory_example_path = ROLE_ROOT / "inventory.ini.example"
    print(f"DEBUG: inventory_example_path = {inventory_example_path}")
    assert inventory_example_path.exists(), f"inventory.ini.example не найден: {inventory_example_path}"