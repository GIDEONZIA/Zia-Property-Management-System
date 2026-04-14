#!/bin/bash

# ✅ Django app names here — only these will be cleaned
APPS=("properties" "transactions" "reports" "account")  # App names

DB_NAME="property_management_system"
DB_USER="gwiternz"
DB_HOST="127.0.0.1"
DB_PORT="5432"

echo "🔁 Resetting migrations for apps: ${APPS[@]}"

# Step 1: Clean migration files
for app in "${APPS[@]}"; do
    MIGRATION_DIR="./$app/migrations"
    
    if [ -d "$MIGRATION_DIR" ]; then
        echo "🧹 Cleaning migrations in: $MIGRATION_DIR"
        
        # Delete all .py files except __init__.py
        find "$MIGRATION_DIR" -type f -name "*.py" ! -name "__init__.py" -delete

        # Delete all compiled Python files
        find "$MIGRATION_DIR" -type f -name "*.pyc" -delete
    else
        echo "⚠️  Migration directory not found for app: $app"
    fi
done

# Step 2: Clear migration history in DB
echo "🗑  Truncating django_migrations table..."
psql -U "$DB_USER" -h "$DB_HOST" -p "$DB_PORT" -d "$DB_NAME" -c "TRUNCATE TABLE django_migrations CASCADE;"

# Step 3: Recreate migrations
echo "🛠 Running makemigrations..."
python manage.py makemigrations

# Step 4: Apply migrations
echo "📦 Running migrate..."
python manage.py migrate

echo "🎉 Migration reset complete!"
