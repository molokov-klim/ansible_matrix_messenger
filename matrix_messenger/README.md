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
admin_email: "admin@example.com"   # Email для Let's Encrypt
```

### Чувствительные данные (хранить в .env)
```bash
ANSIBLE_HOST=192.168.1.100
ANSIBLE_USER=ubuntu
ANSIBLE_PASSWORD=твой_пароль_здесь
MATRIX_ADMIN_PASSWORD=придумай_надежный_пароль
POSTGRES_PASSWORD=еще_один_надежный_пароль
```

## Пример использования
```yaml
- hosts: matrix_servers
  roles:
    - matrix_messenger
```

## Установка
1. Скопируйте `.env.example` в `.env` и заполните своими значениями:
   ```bash
   cp .env.example .env
   nano .env
   ```

2. Загрузите переменные окружения:
   ```bash
   make load-env
   ```

3. Запустите установку:
   ```bash
   make deploy
   ```

## Безопасность
- Все чувствительные данные хранятся в .env файле (не коммитится)
- Публичная конфигурация хранится в git
- Автоматические проверки безопасности перед каждым запуском