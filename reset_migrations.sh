#!/bin/bash

# ✅ List your Django app names here — only these will be cleaned
APPS=("properties" "transactions" "reports" "account")  # Add your app names

echo "🔁 Resetting migrations for apps: ${APPS[@]}"

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

echo "✅ Done cleaning migration files."

echo "🛠 Running makemigrations..."
python manage.py makemigrations

echo "📦 Running migrate..."
python manage.py migrate

echo "🎉 Migration reset complete!"
