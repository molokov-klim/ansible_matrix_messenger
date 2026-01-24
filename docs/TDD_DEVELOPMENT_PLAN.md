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

===
СТАРЫЙ ПЛАН
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
- **Тестирование**: Molecule + Testinfra с Docker/Vagrant драйверами (InSpec убран как избыточный для этого проекта)
- **CI/CD**: GitHub Actions для автоматического тестирования
- **Безопасность**: Ansible Vault + GitHub Secrets + Environment Variables

## План разработки по TDD

### 🚨 Этап 0: Настройка безопасного управления учетными данными (САМЫЙ ВАЖНЫЙ)

**Статус:** Запланировано

**Цель:** Обеспечить безопасный доступ к серверам для всех сценариев использования.

**TDD шаги:**

1. **Красный этап**: Написать тесты безопасности:
   ```python
   # tests/test_security.py
   import os
   import re
   
   def test_no_secrets_in_codebase(host):
       """Проверка, что в кодовой базе нет секретов"""
       # Ищем потенциальные секреты (исключая тесты и примеры)
       cmd = host.run("git grep -iE '(password|secret|key|token|passphrase)' -- ':!tests' ':!examples' ':!docs'")
       assert cmd.rc != 0, "Найдены секреты в кодовой базе!"
   
   def test_environment_variables_validation(host):
       """Проверка валидации переменных окружения"""
       cmd = host.run("bash -c 'source scripts/validate_env.sh && echo $VALIDATION_PASSED'")
       assert cmd.stdout.strip() == "true", "Валидация переменных окружения не пройдена"
   
   def test_ansible_vault_setup(host):
       """Проверка настройки Ansible Vault"""
       assert host.file("secrets.yml").exists, "Файл secrets.yml не найден"
       cmd = host.run("ansible-vault view secrets.yml --vault-password-file=.vault_pass 2>/dev/null")
       assert cmd.rc == 0, "Ansible Vault не настроен или пароль неверный"
   ```

2. **Зеленый этап**: Реализовать безопасное управление кредами:
    - **Локальная разработка**:
      ```bash
      # .env.example (НЕ в коммите!)
      ANSIBLE_SSH_PRIVATE_KEY_FILE=".ssh/id_ed25519"
      ANSIBLE_SSH_USER="matrix_deploy"
      DOMAIN_NAME="matrix.family"
      ```

      ```bash
      # scripts/validate_env.sh
      #!/bin/bash
      set -e
      
      REQUIRED_VARS=(
          "ANSIBLE_SSH_PRIVATE_KEY_FILE"
          "ANSIBLE_SSH_USER"
          "DOMAIN_NAME"
      )
      
      for var in "${REQUIRED_VARS[@]}"; do
          if [ -z "${!var}" ]; then
              echo "ERROR: Required environment variable $var is not set"
              exit 1
          fi
      done
      
      if [ ! -f "$ANSIBLE_SSH_PRIVATE_KEY_FILE" ]; then
          echo "ERROR: SSH private key file not found: $ANSIBLE_SSH_PRIVATE_KEY_FILE"
          exit 1
      fi
      
      chmod 600 "$ANSIBLE_SSH_PRIVATE_KEY_FILE"
      export VALIDATION_PASSED="true"
      ```

    - **GitHub Actions**:
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
                git grep -iE '(password|secret|key|token)' -- ':!tests' ':!examples' && exit 1 || exit 0
            
        test:
          needs: security-check
          runs-on: ubuntu-latest
          env:
            ANSIBLE_SSH_PRIVATE_KEY: ${{ secrets.TESTING_SSH_KEY }}
            MATRIX_ADMIN_PASSWORD: ${{ secrets.MATRIX_ADMIN_PASSWORD }}
          steps:
            - uses: actions/checkout@v4
            - name: Set up Python
              uses: actions/setup-python@v4
              with:
                python-version: '3.11'
            
            - name: Install dependencies
              run: |
                pip install molecule[docker] ansible testinfra
                echo "$ANSIBLE_SSH_PRIVATE_KEY" > id_ed25519
                chmod 600 id_ed25519
            
            - name: Run molecule tests
              run: molecule test
      ```

    - **Ansible Vault для чувствительных данных**:
      ```yaml
      # defaults/main.yml
      matrix_admin_user: "admin"
      matrix_admin_password: !vault |
        $ANSIBLE_VAULT;1.1;AES256
        38393734353637343938373435363734393837343536373439383734353637343938
      ```

3. **Рефакторинг**: Создать единый механизм загрузки окружения:
   ```python
   # plugins/filter/env_loader.py
   from ansible.errors import AnsibleFilterError
   import os
   
   def load_environment():
       """Загружает переменные окружения с валидацией"""
       required_vars = ['ANSIBLE_SSH_USER', 'DOMAIN_NAME']
       
       missing_vars = [var for var in required_vars if not os.getenv(var)]
       if missing_vars:
           raise AnsibleFilterError(f"Missing required environment variables: {', '.join(missing_vars)}")
       
       return {
           'ssh_user': os.getenv('ANSIBLE_SSH_USER'),
           'domain': os.getenv('DOMAIN_NAME'),
           'env': 'github_actions' if os.getenv('GITHUB_ACTIONS') else 'local'
       }
   
   class FilterModule:
       def filters(self):
           return {
               'load_environment': load_environment
           }
   ```

**Критические компоненты безопасности:**

- 🔐 **SSH ключи**: Отдельные ключи для разных окружений (testing/staging/prod)
- 🔐 **Ansible Vault**: Обязательное шифрование всех чувствительных данных
- 🔐 **Environment validation**: Скрипт валидации перед запуском любой операции
- 🔐 **Secrets scanning**: Автоматическая проверка на наличие секретов в CI
- 🔐 **Least privilege**: Учетные записи с минимальными необходимыми правами

**Ожидаемый результат:**

- ✅ **Никаких секретов в репозитории** (проверено в CI)
- ✅ **Единый механизм загрузки окружения** для всех сценариев
- ✅ **Автоматическая валидация** перед запуском операций
- ✅ **Разделение окружений** через переменные окружения
- ✅ **Шифрование чувствительных данных** через Ansible Vault

---

### Этап 1: Настройка инфраструктуры тестирования (Molecule)

**Статус:** Запланировано

**Цель:** Создать рабочую TDD-инфраструктуру с Molecule.

**TDD шаги:**

1. **Красный этап**: Написать тест, который должен упасть:
   ```python
   # molecule/default/tests/test_infrastructure.py
   def test_molecule_infrastructure(host):
       # Этот тест должен упасть, потому что роль еще не создана
       assert host.package("nonexistent-package").is_installed
   ```

2. **Зеленый этап**: Инициализировать проект и настроить Molecule:
   ```bash
   # Инициализация роли
   molecule init role matrix_messenger --driver-name docker
   
   # Настройка molecule.yml
   cat > molecule/default/molecule.yml << EOF
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
           domain_name: "matrix.test"
   verifier:
     name: testinfra
   scenario:
     name: default
   EOF
   ```

3. **Рефакторинг**: Добавить базовые тесты и CI интеграцию:
   ```python
   # molecule/default/tests/test_basic.py
   def test_hosts_file(host):
       f = host.file('/etc/hosts')
       assert f.exists
       assert f.user == 'root'
       assert f.group == 'root'
   
   def test_apt_update(host):
       cmd = host.run("apt list --upgradable 2>/dev/null | grep -v 'Listing...' | wc -l")
       assert int(cmd.stdout.strip()) == 0, "Есть обновления пакетов"
   ```

**Ожидаемый результат:**

- ✅ **Рабочая TDD-инфраструктура** с Molecule
- ✅ **Автоматические тесты** в GitHub Actions
- ✅ **Базовые проверки** для чистой системы
- ✅ **Готовность** к разработке функционала

### Этап 2: Установка и базовая настройка Matrix Synapse

**Статус:** Запланировано

**Цель:** Установить Matrix Synapse и обеспечить базовую работоспособность.

**TDD шаги:**

1. **Красный этап**: Написать тесты для Synapse:
   ```python
   # molecule/default/tests/test_synapse_installation.py
   def test_synapse_package_installed(host):
       assert not host.package("matrix-synapse").is_installed, "Пакет установлен до реализации"
   
   def test_synapse_service_status(host):
       assert not host.service("matrix-synapse").is_running, "Сервис запущен до реализации"
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
       repo: deb https://packages.matrix.org/debian/ {{ ansible_distribution_release }} main
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

3. **Рефакторинг**: Добавить проверку идемпотентности и оптимизировать конфигурацию:
   ```bash
   # Проверка идемпотентности
   molecule converge
   molecule converge  # Должно показать 0 изменений
   ```

**Ожидаемый результат:**

- ✅ **Matrix Synapse установлен и запущен**
- ✅ **Конфигурация соответствует шаблонам**
- ✅ **Роль идемпотентна** (нулевые изменения при повторном запуске)
- ✅ **Базовые API эндпоинты доступны**

### Этап 3: Интеграция с PostgreSQL

**Статус:** Запланировано

**Цель:** Настроить PostgreSQL как основную базу данных для Matrix Synapse.

**TDD шаги:**

1. **Красный этап**: Написать тесты для PostgreSQL интеграции:
   ```python
   # molecule/default/tests/test_postgres_integration.py
   def test_postgres_installed(host):
       assert not host.package("postgresql").is_installed
   
   def test_synapse_database_connection(host):
       config = host.file("/etc/matrix-synapse/homeserver.yaml")
       assert not config.contains("database:")
       assert not config.contains("postgres://")
   ```

2. **Зеленый этап**: Реализовать установку PostgreSQL и интеграцию:
   ```yaml
   # tasks/setup_postgres.yml
   - name: Install PostgreSQL
     apt:
       name: 
         - postgresql
         - postgresql-contrib
         - libpq-dev
       state: present
   
   - name: Create Synapse database user
     postgresql_user:
       name: "{{ matrix_db_user }}"
       password: "{{ matrix_db_password }}"
       role_attr_flags: LOGIN
       encrypted: yes
   
   - name: Create Synapse database
     postgresql_db:
       name: "{{ matrix_db_name }}"
       owner: "{{ matrix_db_user }}"
       encoding: UTF-8
       lc_collate: en_US.UTF-8
       lc_ctype: en_US.UTF-8
       template: template0
   
   - name: Grant privileges to Synapse user
     postgresql_privs:
       database: "{{ matrix_db_name }}"
       roles: "{{ matrix_db_user }}"
       privs: ALL
       type: database
   ```

3. **Рефакторинг**: Вынести чувствительные данные в Ansible Vault и добавить проверки безопасности:
   ```yaml
   # vars/main.yml
   matrix_db_name: "synapse"
   matrix_db_user: "synapse_user"
   matrix_db_password: !vault |
     $ANSIBLE_VAULT;1.1;AES256
     38393734353637343938373435363734393837343536373439383734353637343938
   ```

**Ожидаемый результат:**

- ✅ **PostgreSQL установлен и настроен**
- ✅ **Synapse использует PostgreSQL вместо SQLite**
- ✅ **Чувствительные данные зашифрованы**
- ✅ **Права доступа к базе данных корректны**

### Этап 4: Настройка Nginx и SSL (Let's Encrypt)

**Статус:** Запланировано

**Цель:** Обеспечить безопасный HTTPS доступ через Nginx и автоматические SSL сертификаты.

**TDD шаги:**

1. **Красный этап**: Написать тесты для Nginx и SSL:
   ```python
   # molecule/default/tests/test_nginx_ssl.py
   def test_nginx_not_installed(host):
       assert not host.package("nginx").is_installed
   
   def test_ssl_certificate_missing(host):
       cert_path = f"/etc/letsencrypt/live/{host.ansible.get_variables()['domain_name']}/fullchain.pem"
       assert not host.file(cert_path).exists
   ```

2. **Зеленый этап**: Реализовать установку Nginx и Certbot:
   ```yaml
   # tasks/setup_nginx.yml
   - name: Install Nginx
     apt:
       name: nginx
       state: present
   
   - name: Install Certbot and Nginx plugin
     apt:
       name: 
         - certbot
         - python3-certbot-nginx
       state: present
   
   - name: Configure Nginx for Matrix
     template:
       src: nginx_matrix.conf.j2
       dest: /etc/nginx/sites-available/matrix
       owner: root
       group: root
       mode: '0644'
     notify: Reload Nginx
   
   - name: Enable Nginx site
     file:
       src: /etc/nginx/sites-available/matrix
       dest: /etc/nginx/sites-enabled/matrix
       state: link
   
   - name: Obtain SSL certificate
     command: >
       certbot --nginx --non-interactive --agree-tos
       --email {{ admin_email }}
       -d {{ domain_name }}
       --redirect
     args:
       creates: "/etc/letsencrypt/live/{{ domain_name }}/fullchain.pem"
     register: certbot_result
     failed_when: certbot_result.rc != 0 and "Certificate not yet due for renewal" not in certbot_result.stdout
   ```

3. **Рефакторинг**: Добавить автоматическое обновление сертификатов и проверки безопасности:
   ```yaml
   # handlers/main.yml
   - name: Reload Nginx
     systemd:
       name: nginx
       state: reloaded
   
   # tasks/setup_certbot_cron.yml
   - name: Create Certbot cron job
     cron:
       name: "Renew SSL certificates"
       job: "/usr/bin/certbot renew --quiet --post-hook 'systemctl reload nginx'"
       minute: "0"
       hour: "3"
       day: "*"
       month: "*"
       weekday: "6"
   ```

**Ожидаемый результат:**

- ✅ **Nginx настроен как reverse proxy для Synapse**
- ✅ **SSL сертификаты Let's Encrypt получены и обновляются автоматически**
- ✅ **HTTP трафик перенаправляется на HTTPS**
- ✅ **Конфигурация безопасности Nginx соответствует best practices**

### Этап 5: Создание пользователей и настройка безопасности

**Статус:** Запланировано

**Цель:** Создать административных пользователей и настроить параметры безопасности.

**TDD шаги:**

1. **Красный этап**: Написать тесты для пользователей и безопасности:
   ```python
   # molecule/default/tests/test_users_security.py
   def test_admin_user_not_created(host):
       cmd = host.run("grep 'admin:' /etc/matrix-synapse/homeserver.yaml")
       assert cmd.rc != 0
   
   def test_registration_enabled(host):
       config = host.file("/etc/matrix-synapse/homeserver.yaml")
       assert config.contains("enable_registration: true")
   ```

2. **Зеленый этап**: Реализовать создание пользователей и настройку безопасности:
   ```yaml
   # tasks/setup_users.yml
   - name: Create admin user
     command: >
       register_new_matrix_user
       -u {{ admin_username }}
       -p {{ admin_password }}
       --admin
       http://localhost:8008
     args:
       creates: "/var/lib/matrix-synapse/{{ admin_username }}_created"
     register: admin_user_creation
     failed_when: admin_user_creation.rc != 0 and "already exists" not in admin_user_creation.stderr
   
   - name: Create regular users
     command: >
       register_new_matrix_user
       -u {{ item.username }}
       -p {{ item.password }}
       http://localhost:8008
     loop: "{{ family_users }}"
     args:
       creates: "/var/lib/matrix-synapse/{{ item.username }}_created"
     when: item.password is defined
   
   # tasks/setup_security.yml
   - name: Disable public registration
     lineinfile:
       path: /etc/matrix-synapse/homeserver.yaml
       regexp: '^enable_registration:'
       line: 'enable_registration: false'
       backup: yes
     notify: Restart Synapse
   
   - name: Restrict federation
     blockinfile:
       path: /etc/matrix-synapse/homeserver.yaml
       block: |
         federation_domain_whitelist:
           - "{{ domain_name }}"
       marker: "# {mark} FEDERATION WHITELIST"
       insertafter: "federation_domain_whitelist:"
     notify: Restart Synapse
   ```

3. **Рефакторинг**: Вынести учетные данные в защищенные переменные и добавить аудит:
   ```yaml
   # defaults/main.yml
   admin_username: "admin"
   admin_password: !vault |
     $ANSIBLE_VAULT;1.1;AES256
     38393734353637343938373435363734393837343536373439383734353637343938
   
   family_users:
     - username: "user1"
       password: !vault |
         $ANSIBLE_VAULT;1.1;AES256
         38393734353637343938373435363734393837343536373439383734353637343938
   ```

**Ожидаемый результат:**

- ✅ **Администратор и пользователи созданы**
- ✅ **Публичная регистрация отключена**
- ✅ **Федерация ограничена только доверенными доменами**
- ✅ **Учетные данные надежно защищены**

### Этап 6: Интеграционное тестирование и деплоймент

**Статус:** Запланировано

**Цель:** Проверить работоспособность всей системы и настроить деплоймент.

**TDD шаги:**

1. **Красный этап**: Написать интеграционные тесты:
   ```python
   # molecule/default/tests/test_end_to_end.py
   import requests
   import json
   
   def test_matrix_api_health(host):
       domain = host.ansible.get_variables()['domain_name']
       
       # Проверка доступности API
       response = requests.get(f"https://{domain}/_matrix/client/versions", verify=False)
       assert response.status_code == 200
       assert "versions" in response.json()
   
   def test_user_login(host):
       domain = host.ansible.get_variables()['domain_name']
       admin_user = host.ansible.get_variables()['admin_username']
       admin_pass = host.ansible.get_variables()['admin_password']
       
       payload = {
           "type": "m.login.password",
           "user": admin_user,
           "password": admin_pass
       }
       
       response = requests.post(
           f"https://{domain}/_matrix/client/r0/login",
           data=json.dumps(payload),
           headers={"Content-Type": "application/json"},
           verify=False
       )
       
       assert response.status_code == 200
       assert "access_token" in response.json()
   ```

2. **Зеленый этап**: Настроить деплоймент и мониторинг:
   ```yaml
   # tasks/setup_monitoring.yml
   - name: Install Prometheus Node Exporter
     apt:
       name: prometheus-node-exporter
       state: present
   
   - name: Configure Synapse metrics
     lineinfile:
       path: /etc/matrix-synapse/homeserver.yaml
       regexp: '^enable_metrics:'
       line: 'enable_metrics: true'
       backup: yes
     notify: Restart Synapse
   
   # .github/workflows/deploy.yml
   - name: Deploy to staging
     if: github.ref == 'refs/heads/staging'
     run: |
       ansible-playbook -i staging.inventory playbooks/deploy.yml \
         --private-key ./id_ed25519 \
         --vault-password-file .vault_pass
     env:
       ANSIBLE_SSH_PRIVATE_KEY: ${{ secrets.STAGING_SSH_KEY }}
       VAULT_PASSWORD: ${{ secrets.VAULT_PASSWORD }}
   ```

3. **Рефакторинг**: Добавить процедуры отката и резервного копирования:
   ```yaml
   # tasks/backup.yml
   - name: Create backup directory
     file:
       path: /var/backups/matrix
       state: directory
       owner: root
       group: root
       mode: '0755'
   
   - name: Backup Synapse database
     command: pg_dump synapse > /var/backups/matrix/synapse_{{ ansible_date_time.iso8601_basic_short }}.sql
     register: backup_result
     changed_when: backup_result.rc == 0
   
   - name: Set up backup cron job
     cron:
       name: "Daily Matrix backup"
       job: "/usr/bin/pg_dump synapse > /var/backups/matrix/synapse_$(date +\%Y\%m\%d).sql"
       minute: "0"
       hour: "2"
       day: "*"
       month: "*"
       weekday: "*"
   ```

**Ожидаемый результат:**

- ✅ **Все компоненты работают вместе**
- ✅ **API и пользовательские операции доступны**
- ✅ **Автоматический деплоймент в staging**
- ✅ **Система мониторинга настроена**
- ✅ **Процедуры резервного копирования работают**

### Этап 7: Документирование и финализация

**Статус:** Запланировано

**Цель:** Создать полную документацию и подготовить роль к использованию.

**TDD шаги:**

1. **Красный этап**: Написать тесты для документации:
   ```python
   # tests/test_documentation.py
   import os
   
   def test_readme_exists():
       assert os.path.exists("README.md"), "README.md не найден"
   
   def test_readme_contains_required_sections():
       with open("README.md", "r") as f:
           content = f.read()
       
       required_sections = [
           "# Matrix Messenger Ansible Role",
           "## Требования",
           "## Переменные",
           "## Пример использования",
           "## Тестирование",
           "## Безопасность"
       ]
       
       for section in required_sections:
           assert section in content, f"Отсутствует раздел: {section}"
   
   def test_vault_example_provided():
       assert os.path.exists("examples/vault_password_example"), "Пример vault password не предоставлен"
   ```

2. **Зеленый этап**: Написать документацию:
   ```markdown
   # Matrix Messenger Ansible Role
   
   ## Описание
   Роль для установки и настройки приватного Matrix сервера для семейного использования.
   
   ## Требования
   - Ubuntu 22.04 LTS
   - Ansible 2.9+
   - Доступ к серверу по SSH с правами sudo
   - Доменное имя с настроенными DNS записями
   
   ## Переменные
   ### Обязательные переменные
   ```yaml
   domain_name: "matrix.example.com"  # Ваше доменное имя
   admin_email: "admin@example.com"    # Email для Let's Encrypt
   ```

   ### Чувствительные данные (хранить в Ansible Vault)
   ```yaml
   admin_password: "secure_password_here"  # Пароль администратора
   matrix_db_password: "db_secure_password"  # Пароль базы данных
   ```

   ## Пример использования
   ```yaml
   - hosts: matrix_servers
     vars_files:
       - vars/vault.yml  # Зашифрованные переменные
     roles:
       - matrix_messenger
   ```

   ## Безопасность
    - Все чувствительные данные шифруются через Ansible Vault
    - Публичная регистрация отключена по умолчанию
    - Федерация ограничена только вашим доменом
    - Автоматическое обновление SSL сертификатов
   ```

3. **Рефакторинг**: Создать шаблоны для разных окружений и добавить CONTRIBUTING.md:
   ```markdown
   ## CONTRIBUTING.md
   
   ### Требования к разработке
   1. Все изменения должны проходить через TDD цикл
   2. Перед коммитом запустить: `molecule test`
   3. Никаких секретов в кодовой базе
   4. Документация должна обновляться вместе с кодом
   
   ### Процесс
   1. Создать issue или обсудить изменение
   2. Создать feature branch
   3. Написать тесты (красный этап)
   4. Реализовать функциональность (зеленый этап)
   5. Провести рефакторинг
   6. Создать pull request
   7. Пройти code review
   ```

**Ожидаемый результат:**

- ✅ **Полная и актуальная документация**
- ✅ **Примеры конфигурации для разных сценариев**
- ✅ **Четкие инструкции по безопасности**
- ✅ **Процесс contribution задокументирован**
- ✅ **Роль готова к использованию в продакшене**

## Заключение

Этот TDD-план обеспечивает качество и надежность Ansible роли через:

- 🔐 **Безопасность с первого этапа** - управление учетными данными является приоритетом №1
- 🔄 **Строгий TDD цикл** - для каждого функционального блока сначала пишутся падающие тесты
- 🧪 **Постепенное нарастание сложности** - от базовой инфраструктуры до интеграционных тестов
- 🤖 **Автоматизация всего** - CI/CD, тестирование, деплоймент
- 📚 **Документация как код** - тесты для документации гарантируют её актуальность
- 🔄 **Идемпотентность** - роль может запускаться многократно без побочных эффектов

**Ключевой принцип:** Никакой функциональности без тестов. Если тест нельзя написать - значит, функциональность
спроектирована неправильно.