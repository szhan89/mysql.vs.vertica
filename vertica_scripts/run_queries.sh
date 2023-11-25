DB_USER="dbadmin"
DB_NAME="verticaDB"

echo "Query 1"
vsql -U "$DB_USER" -d "$DB_NAME" -f /home/dbadmin/queries/1.sql

echo "Query 3"
vsql -U "$DB_USER" -d "$DB_NAME" -f /home/dbadmin/queries/3.sql

echo "Query 7"
vsql -U "$DB_USER" -d "$DB_NAME" -f /home/dbadmin/queries/7.sql

echo "Query 14"
vsql -U "$DB_USER" -d "$DB_NAME" -f /home/dbadmin/queries/14.sql

echo "Query 19"
vsql -U "$DB_USER" -d "$DB_NAME" -f /home/dbadmin/queries/19.sql
