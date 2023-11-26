import subprocess
import time

MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
DATABASE_NAME = "TPCH"
DOCKER_CONTAINER_NAME = "mysql-server"
QUERY_DIR = "/etc/tpch/queries"
#SQL_FILES = ["1.sql", "2.sql", "3.sql", "4.sql", "5.sql", "6.sql", "7.sql", "8.sql", "9.sql", "10.sql", "11.sql", "12.sql", "13.sql", "14.sql", "15.sql", "16.sql", "17.sql", "18.sql", "19.sql", "20.sql", "21.sql", "22.sql"] # Update with your SQL file names
SQL_FILES = ["1.sql", "3.sql", "7.sql", "14.sql","19.sql"]
def print_formatted_stats(stats):
    lines = stats.strip().split('\n')
    headers = lines[0].split(maxsplit=7)  # Adjusting maxsplit based on the actual number of columns
    values = lines[1].split(maxsplit=7)

    # Map the headers to user-friendly labels
    stats_labels = {
        "CONTAINER ID": "Container ID",
        "NAME": "Name",
        "CPU %": "CPU Usage",
        "MEM USAGE / LIMIT": "Memory Usage",
        "MEM %": "Memory %",
        "NET I/O": "Network I/O",
        "BLOCK I/O": "Block I/O",
        "PIDS": "PIDs"
    }

    # Construct a dictionary with the labels and values
    formatted_stats = {stats_labels.get(header, header): value for header, value in zip(headers, values)}
    
    # Print each label and its corresponding value
    for label, value in formatted_stats.items():
        print(f"{label}: {value}", end='  ')
    print('\n')  # Add newline for formatting

def enable_stage_instrumentation():
    enable_stage_command = [
        'docker', 'exec', DOCKER_CONTAINER_NAME, 'mysql',
        f'-u{MYSQL_USER}', f'-p{MYSQL_PASSWORD}', '-e',
        "UPDATE performance_schema.setup_instruments SET ENABLED = 'YES', TIMED = 'YES' WHERE NAME LIKE '%stage/%';"
    ]
    subprocess.run(enable_stage_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def enable_performance_schema():
    enable_command = [
        'docker', 'exec', DOCKER_CONTAINER_NAME, 'mysql',
        f'-u{MYSQL_USER}', f'-p{MYSQL_PASSWORD}', '-e',
        'SET GLOBAL performance_schema = ON;'
    ]
    subprocess.run(enable_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def database_reset():
    # Reset the performance schema table
    reset_command = [
        'docker', 'exec', DOCKER_CONTAINER_NAME, 'mysql',
        f'-u{MYSQL_USER}', f'-p{MYSQL_PASSWORD}', '-e',
        "TRUNCATE TABLE performance_schema.table_io_waits_summary_by_table;"
    ]
    subprocess.run(reset_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def database_read():
    # Query to get the total read count
    query = (
        f"SELECT SUM(COUNT_READ) AS total_reads "
        f"FROM performance_schema.table_io_waits_summary_by_table "
        f"WHERE OBJECT_SCHEMA = '{DATABASE_NAME}';"
    )

    query_command = [
        'docker', 'exec', DOCKER_CONTAINER_NAME, 'mysql',
        f'-u{MYSQL_USER}', f'-p{MYSQL_PASSWORD}', '-e',
        query
    ]

    result = subprocess.run(query_command, capture_output=True, text=True)
    
    if result.returncode == 0:
        # Extracting the numeric value from the result
        lines = result.stdout.splitlines()
        if len(lines) > 1 and lines[1].strip().isdigit():
            total_reads = lines[1].strip()
            print(f"The total read for this query is: {total_reads}")
        else:
            print("Unable to parse the total reads from the query result.")
    else:
        print("Error executing query:", result.stderr)

def database_write():
    # Query to get the total read count
    query = (
        f"SELECT SUM(COUNT_WRITE) AS total_writes "
        f"FROM performance_schema.table_io_waits_summary_by_table "
        f"WHERE OBJECT_SCHEMA = '{DATABASE_NAME}';"
    )

    query_command = [
        'docker', 'exec', DOCKER_CONTAINER_NAME, 'mysql',
        f'-u{MYSQL_USER}', f'-p{MYSQL_PASSWORD}', '-e',
        query
    ]

    result = subprocess.run(query_command, capture_output=True, text=True)
    
    if result.returncode == 0:
        # Extracting the numeric value from the result
        lines = result.stdout.splitlines()
        if len(lines) > 1 and lines[1].strip().isdigit():
            total_writes = lines[1].strip()
            print(f"The total writes for this query is: {total_writes}")
        else:
            print("Unable to parse the total writes from the query result.")
    else:
        print("Error executing query:", result.stderr)

def monitor_container():
    command = f"sudo docker stats --no-stream {DOCKER_CONTAINER_NAME}"
    stats = subprocess.check_output(command, shell=True).decode('utf-8')
    print_formatted_stats(stats)

def execute_query_in_docker(sql_file):
    command = f"sudo docker exec {DOCKER_CONTAINER_NAME} sh -c 'mysql -u{MYSQL_USER} -p{MYSQL_PASSWORD} {DATABASE_NAME} < {QUERY_DIR}/{sql_file}'"
    start_time = time.perf_counter()
    subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end_time = time.perf_counter()
    return round(end_time - start_time, 2)

def main():
    enable_performance_schema()  # Enable Performance Schema
    enable_stage_instrumentation()  # Enable stage instrumentation
    for sql_file in SQL_FILES:
        database_reset()
        elapsed_time = execute_query_in_docker(sql_file)
        database_read()
        database_write()
        monitor_container()
        print(f"Query from {sql_file} executed in {elapsed_time} seconds")

if __name__ == "__main__":
    main()
