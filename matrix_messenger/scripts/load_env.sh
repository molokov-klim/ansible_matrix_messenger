#!/bin/bash
set -e

ENV_FILE=".env.test"

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