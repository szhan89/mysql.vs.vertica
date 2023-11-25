import subprocess
import time

MYSQL_USER = "root"
MYSQL_PASSWORD = "root"
DATABASE_NAME = "TPCH"
DOCKER_CONTAINER_NAME = "mysql-server"
QUERY_DIR = "/etc/tpch/queries"
#SQL_FILES = ["1.sql", "2.sql", "3.sql", "4.sql", "5.sql", "6.sql", "7.sql", "8.sql", "9.sql", "10.sql", "11.sql", "12.sql", "13.sql", "14.sql", "15.sql", "16.sql", "17.sql", "18.sql", "19.sql", "20.sql", "21.sql", "22.sql"] # Update with your SQL file names
SQL_FILES = ["1.sql", "2.sql"]
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
    for sql_file in SQL_FILES:
        elapsed_time = execute_query_in_docker(sql_file)
        monitor_container()
        print(f"Query from {sql_file} executed in {elapsed_time} seconds")

if __name__ == "__main__":
    main()
