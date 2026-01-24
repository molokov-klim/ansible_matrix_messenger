# План разработки по TDD для Ansible роли установки приватного семейного мессенджера

## Введение

Этот документ описывает детальный план разработки Ansible роли для установки приватного семейного мессенджера на основе
протокола Matrix. План реализует методологию TDD (Test-Driven Development) с использованием фреймворка **Molecule** для
тестирования ролей, где сначала пишутся тесты (красный этап), затем реализуется функциональность (зеленый этап), и
наконец проводится рефакторинг.

## Архитектура решения

- **Core**: Matrix Synapse сервер
- **Прокси**: Nginx с автоматическим SSL (Let's Encrypt)
- **База данных**: PostgreSQL для хранения данных Matrix
- **Тестирование**: Molecule + Testinfra с Docker драйвером
- **CI/CD**: GitHub Actions для автоматического тестирования
- **Безопасность**: Переменные среды для секретов + простая валидация
- **Переменные среды**: Используются для конфигурации окружения и безопасного хранения чувствительных данных

## План разработки по TDD

### 🚨 Этап 0: Настройка безопасного управления учетными данными (САМЫЙ ВАЖНЫЙ)

**Статус:** Запланировано

**Цель:** Обеспечить безопасный доступ к серверам для всех сценариев использования.

**TDD подход к переменным среды:**

1. **Красный этап**: Написать тесты для проверки наличия обязательных переменных среды:
   ```python
   # tests/test_environment.py
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
   ```

2. **Зеленый этап**: Реализовать использование переменных среды:
   ```bash
   # .env.example (НИКОГДА НЕ КОММИТИТЬ!)
   # Адрес твоего сервера дома (IP или hostname)
   ANSIBLE_HOST=192.168.1.100

   # Пользователь на сервере (обычно ubuntu или pi)
   ANSIBLE_USER=ubuntu

   # Пароль от этого пользователя
   ANSIBLE_PASSWORD=твой_пароль_от_сервера

   # Пароль админа мессенджера (придумай хороший)
   MATRIX_ADMIN_PASSWORD=SuperParol123

   # Пароль для базы данных (любой надежный)
   POSTGRES_PASSWORD=ParolDB456
   ```

   ```yaml
   # group_vars/matrix_servers.yml (МОЖНО КОММИТИТЬ)
   # Домен
   domain_name: "matrix.molokov"

   # Email для восстановления
   admin_email: "ultrakawaii9654449192@gmail.com"
   ```

3. **Рефакторинг**: Создать скрипт валидации переменных среды:
   ```bash
   # scripts/validate_env.sh
   #!/bin/bash
   set -e

   REQUIRED_VARS=(
       "ANSIBLE_HOST"
       "ANSIBLE_USER"
       "ANSIBLE_PASSWORD"
       "MATRIX_ADMIN_PASSWORD"
       "POSTGRES_PASSWORD"
   )

   for var in "${REQUIRED_VARS[@]}"; do
       if [ -z "${!var}" ]; then
           echo "ERROR: Required environment variable $var is not set"
           exit 1
       fi
   done

   echo "Все обязательные переменные среды установлены"
   ```

**TDD шаги:**

1. **Красный этап**: Написать тесты безопасности:
   ```python
   # tests/test_security.py
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
   ```

2. **Зеленый этап**: Реализовать безопасное управление кредами:

   **Шаг 1: Создать `.env.example` (пример для пользователя):**
   ```bash
   # .env.example
   # СКОПИРУЙ ЭТОТ ФАЙЛ В .env И ЗАПОЛНИ СВОИМИ ЗНАЧЕНИЯМИ
   # НИКОГДА НЕ КОММИТЬ .env ФАЙЛ!
   
   # Доступ к серверу
   ANSIBLE_HOST=192.168.1.100
   ANSIBLE_USER=ubuntu
   ANSIBLE_PASSWORD=твой_пароль_здесь
   
   # Пароли для Matrix
   MATRIX_ADMIN_PASSWORD=придумай_надежный_пароль
   POSTGRES_PASSWORD=еще_один_надежный_пароль
   ```

   **Шаг 2: Создать скрипт загрузки переменных:**
   ```bash
   # scripts/load_env.sh
   #!/bin/bash
   set -e
   
   ENV_FILE=".env"
   
   if [ ! -f "$ENV_FILE" ]; then
       echo "❌ Файл $ENV_FILE не найден!"
       echo "👉 Скопируй .env.example в .env и заполни своими значениями:"
       echo "   cp .env.example .env"
       echo "   nano .env"
       exit 1
   fi
   
   # Загружаем переменные
   export $(grep -v '^#' "$ENV_FILE" | xargs)
   
   # Проверяем обязательные переменные
   REQUIRED_VARS=(
       "ANSIBLE_HOST"
       "ANSIBLE_USER"
       "ANSIBLE_PASSWORD"
       "MATRIX_ADMIN_PASSWORD"
       "POSTGRES_PASSWORD"
   )
   
   for var in "${REQUIRED_VARS[@]}"; do
       if [ -z "${!var}" ]; then
           echo "❌ Обязательная переменная $var не установлена в $ENV_FILE"
           exit 1
       fi
   done
   
   echo "✅ Переменные окружения успешно загружены"
   ```

   **Шаг 3: Создать публичный конфиг (можно коммитить):**
   ```yaml
   # defaults/main.yml
   ---
   # Эти настройки можно хранить в git
   domain_name: "matrix.molokov"
   admin_email: "ultrakawaii9654449192@gmail.com"
   
   # Технические настройки
   matrix_port: 8008
   nginx_port: 80
   ```

   **Шаг 4: Настроить inventory для Ansible:**
   ```ini
   # inventory.ini
   [matrix_servers]
   {{ lookup('env', 'ANSIBLE_HOST') }}
   
   [matrix_servers:vars]
   ansible_user={{ lookup('env', 'ANSIBLE_USER') }}
   ansible_password={{ lookup('env', 'ANSIBLE_PASSWORD') }}
   ansible_connection=ssh
   ansible_ssh_common_args='-o StrictHostKeyChecking=no'
   ```

   **Шаг 5: Настроить простой CI pipeline:**
   ```yaml
   # .github/workflows/ci.yml
   name: CI Pipeline
   
   on: [push, pull_request]
   
   jobs:
     security-check:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         
         - name: Check for secrets in code
           run: |
             # Проверяем, что в коде нет секретов
             git grep -iE '(password|secret|key|token|ANSIBLE_PASSWORD|MATRIX_ADMIN_PASSWORD|POSTGRES_PASSWORD)' \
               -- ':!tests' ':!scripts' ':!.github' ':!.env.example' && exit 1 || exit 0
   
     test:
       needs: security-check
       runs-on: ubuntu-latest
       # Для тестов используем тестовые значения
       env:
         ANSIBLE_HOST: localhost
         ANSIBLE_USER: root
         ANSIBLE_PASSWORD: test_password
         MATRIX_ADMIN_PASSWORD: test_admin_pass
         POSTGRES_PASSWORD: test_db_pass
       steps:
         - uses: actions/checkout@v4
         
         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.11'
         
         - name: Install dependencies
           run: |
             pip install molecule[docker] ansible testinfra
         
         - name: Run molecule tests
           run: |
             molecule test
   ```

3. **Рефакторинг**: Создать удобный интерфейс для работы:
   ```bash
   # Makefile (для удобства)
   load-env:
   	@bash scripts/load_env.sh
   
   test:
   	@source .env && molecule test
   
   deploy:
   	@source .env && ansible-playbook -i inventory.ini site.yml
   
   .PHONY: load-env test deploy
   ```

**Критические компоненты безопасности:**

- 🔐 **Разделение секретов и конфигов** - секреты только в `.env`, конфиги в git
- 🔐 **Автоматическая проверка** - CI сканирует код на наличие секретов
- 🔐 **Простота** - никаких SSH ключей, vault, сложных схем для домашнего использования
- 🔐 **Валидация** - скрипт проверяет наличие всех обязательных переменных
- 🔐 **Документация** - `.env.example` показывает что и как заполнять
- 🔐 **Использование переменных среды** - все чувствительные данные передаются через переменные среды

**Ожидаемый результат:**

- ✅ **Никаких секретов в git** (проверяется в CI)
- ✅ **Простая загрузка переменных** через один скрипт
- ✅ **Четкое разделение** между секретами и публичной конфигурацией
- ✅ **Рабочий доступ** к серверу через логин/пароль
- ✅ **Автоматические проверки** безопасности перед каждым коммитом
- ✅ **Использование переменных среды** для безопасного хранения чувствительных данных

---

### Этап 1: Настройка инфраструктуры тестирования (Molecule)

**Статус:** Запланировано

**Цель:** Создать рабочую TDD-инфраструктуру с Molecule.

**TDD шаги:**

1. **Красный этап**: Написать тест, который должен упасть:
   ```python
   # molecule/default/tests/test_infrastructure.py
   def test_infrastructure_not_ready(host):
       # Этот тест должен упасть, потому что ничего еще не установлено
       assert not host.package("matrix-synapse").is_installed
       assert not host.service("matrix-synapse").is_running
   ```

2. **Зеленый этап**: Инициализировать проект и настроить Molecule:
   ```bash
   # Инициализация роли
   molecule init role matrix_messenger --driver-name docker
   
   # Настройка molecule.yml для простого тестирования
   cat > molecule/default/molecule.yml << EOF
   ---
   dependency:
     name: galaxy
   driver:
     name: docker
   platforms:
     - name: matrix-test
       image: geerlingguy/docker-ubuntu2204-ansible:latest
       pre_build_image: true
       groups:
         - matrix_servers
   provisioner:
     name: ansible
     inventory:
       group_vars:
         matrix_servers:
           ansible_user: root
           # Используем публичные настройки из defaults
           domain_name: "{{ domain_name }}"
           admin_email: "{{ admin_email }}"
   verifier:
     name: testinfra
   scenario:
     name: default
   EOF
   ```

3. **Рефакторинг**: Добавить базовые тесты:
   ```python
   # molecule/default/tests/test_basic.py
   def test_system_is_ubuntu(host):
       assert host.system_info.distribution == "ubuntu"
       assert host.system_info.release == "22.04"
   
   def test_python_installed(host):
       assert host.package("python3").is_installed
   ```

**Ожидаемый результат:**

- ✅ **Рабочая TDD-инфраструктура** с Molecule
- ✅ **Базовые проверки** для чистой Ubuntu 22.04 системы
- ✅ **Интеграция с CI** через GitHub Actions
- ✅ **Готовность** к разработке функционала

### Этап 2: Установка и базовая настройка Matrix Synapse

**Статус:** Запланировано

**Цель:** Установить Matrix Synapse и обеспечить базовую работоспособность.

**TDD шаги:**

1. **Красный этап**: Написать тесты для Synapse:
   ```python
   # molecule/default/tests/test_synapse_installation.py
   def test_synapse_not_installed(host):
       assert not host.package("matrix-synapse").is_installed
   
   def test_synapse_config_missing(host):
       assert not host.file("/etc/matrix-synapse/homeserver.yaml").exists
   ```

2. **Зеленый этап**: Реализовать установку Synapse:
   ```yaml
   # tasks/install_synapse.yml
   - name: Add Matrix.org repository key
     apt_key:
       url: https://packages.matrix.org/debian/matrix-org-archive-keyring.gpg
       state: present
   
   - name: Add Matrix.org repository
     apt_repository:
       repo: "deb https://packages.matrix.org/debian/ {{ ansible_distribution_release }} main"
       state: present
       filename: matrix-org
   
   - name: Install Matrix Synapse
     apt:
       name: matrix-synapse
       state: present
       update_cache: yes
   
   - name: Configure Synapse server name
     template:
       src: homeserver.yaml.j2
       dest: /etc/matrix-synapse/homeserver.yaml
       owner: root
       group: root
       mode: '0644'
     notify: Restart Synapse
   
   - name: Start and enable Matrix Synapse
     systemd:
       name: matrix-synapse
       state: started
       enabled: yes
   ```

   ```yaml
   # handlers/main.yml
   - name: Restart Synapse
     systemd:
       name: matrix-synapse
       state: restarted
   ```

   ```yaml
   # templates/homeserver.yaml.j2
   server_name: "{{ domain_name }}"
   pid_file: /var/run/matrix-synapse.pid
   web_client: true
   
   listeners:
     - port: 8008
       tls: false
       type: http
       x_forwarded: true
       resources:
         - names: [client, federation]
           compress: false
   
   database:
     name: sqlite
     args:
       database: /var/lib/matrix-synapse/homeserver.db
   
   log_config: "/etc/matrix-synapse/log_config.yaml"
   
   media_store_path: "/var/lib/matrix-synapse/media_store"
   
   # Email для восстановления пароля
   account_validity:
     renew_email_subject: "Обновление аккаунта на {{ domain_name }}"
   ```

3. **Рефакторинг**: Добавить проверку идемпотентности:
   ```bash
   # Проверка идемпотентности
   molecule converge
   molecule converge  # Должно показать 0 изменений
   ```

**Ожидаемый результат:**

- ✅ **Matrix Synapse установлен и запущен**
- ✅ **Конфигурация использует наши переменные** (domain_name, admin_email)
- ✅ **Роль идемпотентна** (нулевые изменения при повторном запуске)
- ✅ **Базовый веб-интерфейс доступен** на порту 8008

### Этапы 3-7 остаются практически без изменений, так как они уже используют правильный подход:

- **Этап 3 (PostgreSQL)**: Будет использовать `{{ lookup('env', 'POSTGRES_PASSWORD') }}` для пароля из переменных среды
- **Этап 4 (Nginx/SSL)**: Будет использовать `{{ domain_name }}` и `{{ admin_email }}` из публичного конфига
- **Этап 5 (Пользователи)**: Будет использовать `{{ lookup('env', 'MATRIX_ADMIN_PASSWORD') }}` для пароля админа
- **Этапы 6-7**: Интеграционные тесты и документация будут использовать тот же подход
