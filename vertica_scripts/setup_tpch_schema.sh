# Executes on Docker

# Variables
VERTICA_BIN_DIR="/opt/vertica/bin"
VERTICA_DB="verticaDB"
VERTICA_USER="dbadmin"
TPCH_SCHEMA_FILE="/home/dbadmin/scripts/tpch_schema.sql"
TBL_TO_TPCH="/home/dbadmin/scripts/tbl_to_tpch.sql"

# Create the TPC-H schema using vsql
echo "Creating TPC-H schema in Vertica database $VERTICA_DB..."

$VERTICA_BIN_DIR/vsql -U $VERTICA_USER -d $VERTICA_DB -f $TPCH_SCHEMA_FILE

$VERTICA_BIN_DIR/vsql -U $VERTICA_USER -d $VERTICA_DB -f $TBL_TO_TPCH


echo "TPCH-H schema creation completed."