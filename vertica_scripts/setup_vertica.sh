# Executes on docker

# Variables
VERTICA_BIN_DIR="/opt/vertica/bin"
DB_NAME="verticaDB"
DB_NODES="v_vmart_node0001"
DB_CONFIG_FILE="/home/dbadmin/verticaDB.conf"


# Initialize Vertica
echo 'Initializing Vertica...'
/opt/vertica/sbin/install_vertica --hosts $DB_NODES --failure-threshold NONE

# Create the database
echo 'Creating database...'
$VERTICA_BIN_DIR/adminTools -t create_db -s $DB_NODES -d $DB_NAME -c $DB_CONFIG_FILE

# Start the database
echo 'Starting database...'
$VERTICA_BIN_DIR/adminTools -t start_db -d $DB_NAME

echo 'Vertica database setup completed.'
