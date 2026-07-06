#!/bin/bash
set -e

DB_HOST="${HOST:-db}"
DB_USER="${USER:-odoo}"
DB_PASSWORD="${PASSWORD:-odoo17}"
DB_NAME="${DB_NAME:-pos_test}"
DB_PORT="${DB_PORT:-5432}"
POS_DEMO="${POS_DEMO:-false}"

INIT_MODULES="base,web,point_of_sale"
if [ "$POS_DEMO" = "true" ]; then
  INIT_MODULES="${INIT_MODULES},pos_demo"
fi

# Check if psql is available and DB is initialized (skip check if psql not found)
NEED_INIT=true
if command -v psql &>/dev/null; then
  TABLE_EXISTS=$(PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -t -c "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name='ir_module_module');" 2>/dev/null || echo "f")
  if [ "$TABLE_EXISTS" = "t" ]; then
    NEED_INIT=false
  fi
else
  echo "psql not found; skipping DB check, will run init unconditionally."
fi

if [ "$NEED_INIT" = "true" ]; then
  echo "Initializing Odoo database with Point of Sale module..."

  /usr/bin/odoo \
    --db_host="$DB_HOST" \
    --db_user="$DB_USER" \
    --db_password="$DB_PASSWORD" \
    --database="$DB_NAME" \
    --db_port="$DB_PORT" \
    --init="$INIT_MODULES" \
    --stop-after-init \
    --no-http \
    --log-level=info \
    2>&1

  INIT_EXIT_CODE=$?
  if [ $INIT_EXIT_CODE -ne 0 ]; then
    echo "ERROR: Odoo database initialization failed with exit code $INIT_EXIT_CODE"
    exit $INIT_EXIT_CODE
  fi

  echo "Database initialized with POS module and demo data."
else
  echo "Database already initialized. Skipping setup."
fi

echo "Starting Odoo server..."
exec /usr/bin/odoo \
  --db_host="$DB_HOST" \
  --db_user="$DB_USER" \
  --db_password="$DB_PASSWORD" \
  --database="$DB_NAME" \
  --db_port="$DB_PORT" \
  --http-port=8069 \
  --log-level=info \
  --workers=4 \
  --max-cron-threads=2 \
  
