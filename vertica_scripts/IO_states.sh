DB_USER="dbadmin"
DB_NAME="verticaDB"

read -r Timing is on Pager usage is off transaction_id statement_id <<<$(vsql -U "$DB_USER" -d "$DB_NAME" -At -c "SELECT transaction_id, statement_id FROM v_monitor.query_requests LIMIT 1;")
echo "Reading done"

if [[ -z "$transaction_id" ]] || [[ -z "$statement_id" ]]; then
    echo "No recent query found or unable to retrive the IDs."
    exit 1
fi

echo "$transaction_id"
echo "$statement_id"
vsql -U "$DB_USER" -d "$DB_NAME" -At -c "SELECT input_rows, output_rows FROM v_monitor.query_consumption WHERE transaction_id = '$transaction_id' AND statement_id = '$statement_id';"