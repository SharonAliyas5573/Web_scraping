from fastapi import FastAPI, Depends
from fastapi.staticfiles import StaticFiles
import mysql.connector
from datetime import datetime
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
import os
import time

# Create the FastAPI app
app = FastAPI()

# Set up the database connection
load_dotenv()

host = os.environ.get('MYSQL_HOST')
user = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
database = os.environ.get('MYSQL_DATABASE')

try:
    db = mysql.connector.connect(user=user, password=password,
                                host=host,
                                database=database)

except mysql.connector.Error as err:
    db = None
    print(f"Error connecting to database: {err}")

# Define a function to get a database cursor
def get_cursor():
    while True:
        try:
            db = mysql.connector.connect(user=user, password=password,
                                          host=host, database=database)
            cursor = db.cursor(dictionary=True)
            yield cursor
            cursor.close()
            db.close()
            break  # exit the loop if the connection was successful
        except mysql.connector.Error as e:
            print(f"Failed to connect to database: {e}. Retrying in 5 seconds...")
            time.sleep(5)  

# Mount the static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the index.html file
@app.get("/", response_class=HTMLResponse)
async def root():
    with open("static/index.html", "r") as f:
        return f.read()

# Define the API route to fetch news
@app.get("/news")
async def get_news(cursor=Depends(get_cursor)):
    try:
        cursor.execute("SELECT * FROM news")
        news = cursor.fetchall()
        return [{"heading": n["heading"], "content": n["content"], "image_url": n["image_url"],"source_tag": n["source_tag"]} for n in news]

    except mysql.connector.Error as err:
        print(f"Error executing query: {err}")
        return []

def get_crawler_status(crawler_name):
    try:
        with open(f"../scripts/{crawler_name}.log", "r") as f:
            lines = f.readlines()
            status = "".join(lines[-5:])
    except FileNotFoundError:
        status = f"{crawler_name} log file not found"
    
    return status

@app.get("/status")
async def get_status():
    # Check the status of the database connection
    if db is None:
        db_status = "Not connected to database"
    else:
        try:
            db.is_connected()
            db_status = "Connected to MySQL database"
        
        except mysql.connector.Error as err:
            db_status = f"Error connecting to database: {err}"
    

   # Check the status of the crawlers
    scraper1_status = get_crawler_status("crawler1")
    scraper2_status = get_crawler_status("crawler2")
    scraper3_status = get_crawler_status("crawler3")
    # Create a dictionary with the status information
    status_dict = {
        "database": db_status,
        "scraper1": scraper1_status,
        "scraper2": scraper2_status,
        "scraper3": scraper3_status,
        "timestamp": str(datetime.now())
    }

    # Return the status dictionary as a JSON response
    return status_dict

