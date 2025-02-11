#!/bin/bash

# Директория для хранения бэкапов
BACKUP_DIR="/root/backups"

# Создаем директорию если её нет
mkdir -p $BACKUP_DIR

# Имя Docker контейнера
CONTAINER_NAME="crypto_django_aiogram_bot"

# Текущая дата для имени файла
DATE=$(date +%Y-%m-%d_%H-%M-%S)

# Создаем бэкап базы данных
echo "Starting database backup..."
docker cp $CONTAINER_NAME:/app/db.sqlite3 $BACKUP_DIR/backup_$DATE.sqlite3

# Оставляем только последние 7 бэкапов
cd $BACKUP_DIR
ls -t | tail -n +8 | xargs -r rm

echo "Backup completed: $BACKUP_DIR/backup_$DATE.sqlite3"
