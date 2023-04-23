import mysql.connector.pooling
from dotenv import load_dotenv
import os
load_dotenv()

import mysql.connector

# establish connection
conn = mysql.connector.connect(
    host='172.17.0.2',
   
    user='sharon',
    password='password',
    database='web_scrape'
)

# check connection status
if conn.is_connected():
    print('Connected to MySQL database')
else:
    print('Connection failed')

