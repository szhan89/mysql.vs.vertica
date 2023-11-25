SELECT
    transaction_id INTO current_transaction_id
    statement_id INTO current_statement_id
FROM
    v_monitor.query_requests
LIMIT 1;

SELECT
    data_bytes_read,
    data_bytes_written
FROM
    v_monitor.query_consumption
WHERE
    transaction_id = current_transaction_id
    statement_id = current_statement_id;