echo "Running database migrations..."
python app/scripts/create_tables.py

echo "Checking if data exists..."
python -c "
from app.core.database import get_engine
from sqlalchemy import text
engine = get_engine()
with engine.connect() as conn:
    count = conn.execute(text('SELECT COUNT(*) FROM product_inspections')).scalar()
    print(f'Found {count} records')
    exit(0 if count > 0 else 1)
"

if [ $? -eq 1 ]; then
    echo "No data found, ingesting..."
    python app/scripts/ingest_data.py
else
    echo "Data already exists, skipping ingest."
fi

echo "Starting server..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000