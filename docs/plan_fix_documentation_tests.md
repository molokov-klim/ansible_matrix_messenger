# План по исправлению ошибки в тестах документации

## Причина ошибки

Тесты документации в `matrix_messenger/molecule/default/tests/test_documentation.py` ищут файлы в неправильной директории. 
Вместо корня проекта (`/home/runner/work/ansible_matrix_messenger/ansible_matrix_messenger/`) 
они ищут файлы в поддиректории роли (`/home/runner/work/ansible_matrix_messenger/ansible_matrix_messenger/matrix_messenger/`).

## Проблема в определении пути

В тесте используется:
```python
ROLE_ROOT = pathlib.Path(__file__).parent.parent.parent.resolve()
```

Это приводит к:
- `__file__` = `/home/runner/work/.../matrix_messenger/molecule/default/tests/test_documentation.py`
- `.parent` = `/home/runner/work/.../matrix_messenger/molecule/default/tests/`
- `.parent.parent` = `/home/runner/work/.../matrix_messenger/molecule/default/`
- `.parent.parent.parent` = `/home/runner/work/.../matrix_messenger/molecule/`

Но нам нужен путь к корню проекта: `/home/runner/work/ansible_matrix_messenger/ansible_matrix_messenger/`

## Решение

### Вариант 1: Использовать относительный путь от корня роли

Изменить определение `ROLE_ROOT` в тесте:
```python
# Вместо:
ROLE_ROOT = pathlib.Path(__file__).parent.parent.parent.resolve()

# Использовать:
ROLE_ROOT = pathlib.Path(__file__).parent.parent.parent.parent.resolve()
```

Это даст нам:
- `.parent.parent.parent.parent` = `/home/runner/work/ansible_matrix_messenger/ansible_matrix_messenger/`

### Вариант 2: Использовать переменную окружения

Определить путь к корню проекта через переменную окружения в CI и использовать её в тестах.

### Вариант 3: Использовать фиксированный путь

В тестах использовать фиксированный путь к корню проекта, например:
```python
PROJECT_ROOT = pathlib.Path("/home/runner/work/ansible_matrix_messenger/ansible_matrix_messenger/")
```

Это менее гибкий подход, но работает в CI.

## Рекомендуемое решение

Использовать Вариант 1, так как он:
- Сохраняет переносимость тестов
- Не зависит от переменных окружения
- Корректно работает в разных средах

## План действий

1. Обновить `matrix_messenger/molecule/default/tests/test_documentation.py` с правильным определением пути
2. Проверить, что все файлы документации находятся в корне проекта
3. Запустить тесты локально для проверки
4. Закоммитить изменения
5. Запустить CI для проверки

## Дополнительные проверки

После исправления пути, также нужно убедиться, что:
- Все файлы документации находятся в корне проекта
- Тесты не ищут файлы, которые не существуют
- Тесты не зависят от внешних сервисов (как было с matrix.test)