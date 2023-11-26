SELECT
    input_rows,
    output_rows,
    duration_ms
FROM
    v_monitor.query_consumption
ORDER BY
    end_time DESC
LIMIT 10;