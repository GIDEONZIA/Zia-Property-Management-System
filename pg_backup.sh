#!/bin/bash

DB_NAME="property_management_system"
DB_USER="gwiternz"
DB_HOST="localhost"
DB_PORT="5432"
BACKUP_DIR="$HOME/db_backups"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
FILENAME="${DB_NAME}_backup_$DATE.sql"

# Create backup directory if not exists
mkdir -p "$BACKUP_DIR"

echo "🔄 Starting backup for database: $DB_NAME"

PGPASSWORD='@#93Gwiternz29#@' pg_dump -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -F p "$DB_NAME" > "$BACKUP_DIR/$FILENAME"

if [ $? -eq 0 ]; then
    echo "✅ Backup successful: $BACKUP_DIR/$FILENAME"
else
    echo "❌ Backup failed for database: $DB_NAME"
fi

