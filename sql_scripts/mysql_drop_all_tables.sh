#!/bin/bash

# MySQL user, password
MYSQL_USER="root"
MYSQL_PASSWORD="root"

# MySQL Docker container name
DOCKER_CONTAINER_NAME="mysql-server"

# Database name to drop
DATABASE_NAME="TPCH"

# Drop the database
echo "Dropping database: $DATABASE_NAME"
docker exec $DOCKER_CONTAINER_NAME mysql -u$MYSQL_USER -p$MYSQL_PASSWORD -e "DROP DATABASE IF EXISTS $DATABASE_NAME"

echo "Database $DATABASE_NAME dropped."
