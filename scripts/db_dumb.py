import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv
import schedule
import time

# Load the .env file
load_dotenv()

# Retrieve the database name from the environment variables
database_name = os.environ.get('MYSQL_DATABASE')
def perform_backup():
    # Generate the file name with date and time
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"sql_db_dump_{current_datetime}.sql"
    file_path = f"/tmp/{file_name}"
    # Determine the appropriate command based on the database system
    db_engine = os.environ.get('DATABASE_ENGINE')
    if db_engine == 'mysql':
        command = f"mysqldump -u {os.environ.get('MYSQL_USER')} -p{os.environ.get('MYSQL_PASSWORD')} {database_name} > {file_path}"
    else:
        print("Unsupported database engine.")
        exit(1)
    # Execute the database backup command
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Database backup successful. File saved at: {file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error executing the backup command: {e}")
    
    
    
# Schedule the backup every 5 hours
schedule.every(5).hours.do(perform_backup)

# Keep the script running to continue executing scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)
