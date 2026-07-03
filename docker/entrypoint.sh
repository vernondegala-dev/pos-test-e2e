#!/bin/bash
set -e

DB_PORT="${DB_PORT:-5432}"

# Check if the database is properly initialized by looking for the ir_module_module table
TABLE_EXISTS=$(PGPASSWORD=odoo17 psql -h db -U odoo -d pos_test -t -c "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name='ir_module_module');" 2>/dev/null || echo "f")

if [ "$TABLE_EXISTS" != "t" ]; then
  echo "Initializing Odoo database with Point of Sale module..."

  /usr/bin/odoo \
    --db_host=db \
    --db_user=odoo \
    --db_password=odoo17 \
    --database=pos_test \
    --db_port="$DB_PORT" \
    --init=base,web,point_of_sale \
    --stop-after-init \
    --no-http \
    --log-level=info \
    --addons-path=/usr/lib/python3/dist-packages/odoo/addons 2>&1

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
  --db_host=db \
  --db_user=odoo \
  --db_password=odoo17 \
  --database=pos_test \
  --db_port="$DB_PORT" \
  --http-port=8069 \
  --log-level=info \
  --workers=4 \
  --max-cron-threads=2 \
  --addons-path=/usr/lib/python3/dist-packages/odoo/addons
