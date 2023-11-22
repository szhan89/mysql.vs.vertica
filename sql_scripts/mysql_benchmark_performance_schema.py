import subprocess
import time

'''
This scirpt require further modification to work properly. --charlesz

'''

# Database configurations
MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
DATABASE_NAME = "TPCH"
DOCKER_CONTAINER_NAME = "mysql-server"
QUERY_DIR = "/etc/tpch/queries"
SQL_FILES = ["2.sql"]  # List your SQL file names

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
'''
Not Working Properly
note: need better way to located event_id for a query
'''
def fetch_event_id():
    fetch_event_id_command = [
        'docker', 'exec', DOCKER_CONTAINER_NAME, 'mysql',
        f'-u{MYSQL_USER}', f'-p{MYSQL_PASSWORD}', f'{DATABASE_NAME}',
        '-e', "SELECT EVENT_ID FROM performance_schema.events_statements_history_long ORDER BY EVENT_ID DESC LIMIT 1 OFFSET 3;"
    ]
    result = subprocess.run(fetch_event_id_command, capture_output=True, text=True)
    return result.stdout.strip()
'''
Not Working Properly
note: might consiedr to obtain I/O instead of stage time
'''
def fetch_stage_data(event_id):
    # Command to get the stage information for the specific event ID
    fetch_stage_command = [
        'docker', 'exec', DOCKER_CONTAINER_NAME, 'mysql',
        f'-u{MYSQL_USER}', f'-p{MYSQL_PASSWORD}', f'{DATABASE_NAME}', '-e',
        f"SELECT event_id, EVENT_NAME, SOURCE, TIMER_END - TIMER_START FROM performance_schema.events_stages_history_long WHERE NESTING_EVENT_ID = {event_id};"
    ]
    result = subprocess.run(fetch_stage_command, capture_output=True, text=True)
    return result.stdout

def execute_query_in_docker(sql_file):
    # Command to read the SQL query from the file inside the Docker container
    read_query_command = [
        'docker', 'exec', DOCKER_CONTAINER_NAME, 'cat', f"{QUERY_DIR}/{sql_file}"
    ]

    query_result = subprocess.run(read_query_command, capture_output=True, text=True)
    if query_result.stderr:
        print("Error reading SQL file:", query_result.stderr)
        return None

    sql_query = query_result.stdout

    # Now execute the query
    start_time = time.time()
    execute_command = [
        'docker', 'exec', DOCKER_CONTAINER_NAME, 'mysql',
        f'-u{MYSQL_USER}', f'-p{MYSQL_PASSWORD}', f'{DATABASE_NAME}', '-e', sql_query
    ]
    subprocess.run(execute_command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    end_time = time.time()
    elapsed_time = round(end_time - start_time, 2)

    # Fetch stage data after executing the query
    event_id = fetch_event_id()
    if event_id:
        stage_data = fetch_stage_data(event_id)
    else:
        stage_data = "No stage data found"
    return elapsed_time, stage_data

def main():
    
    enable_performance_schema()  # Enable Performance Schema
    enable_stage_instrumentation()  # Enable stage instrumentation
    for sql_file in SQL_FILES:
        elapsed_time,stage_data = execute_query_in_docker(sql_file)
        print(f"Query from {sql_file} executed in {elapsed_time} seconds")
        print(stage_data)

if __name__ == "__main__":
    main()