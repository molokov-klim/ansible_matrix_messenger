#!/bin/bash
# Скрипт для исправления прав доступа к директории Matrix Synapse

echo "Исправление прав доступа к директории Matrix Synapse..."

# Установка правильного владельца для директории данных
sudo chown -R matrix-synapse:matrix-synapse /var/lib/matrix-synapse/

# Установка правильных разрешений
sudo chmod -R 755 /var/lib/matrix-synapse/

# Проверка, что директории существуют и имеют правильные права
if [ ! -d "/var/lib/matrix-synapse/media" ]; then
    sudo mkdir -p /var/lib/matrix-synapse/media
    sudo chown matrix-synapse:matrix-synapse /var/lib/matrix-synapse/media
fi

if [ ! -d "/var/lib/matrix-synapse/uploads" ]; then
    sudo mkdir -p /var/lib/matrix-synapse/uploads
    sudo chown matrix-synapse:matrix-synapse /var/lib/matrix-synapse/uploads
fi

echo "Права доступа исправлены. Теперь можно запустить сервис Matrix Synapse."