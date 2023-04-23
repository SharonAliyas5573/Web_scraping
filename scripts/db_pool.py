import mysql.connector.pooling
from dotenv import load_dotenv
import os

load_dotenv()

host = os.environ.get('MYSQL_HOST')
user = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
database = os.environ.get('MYSQL_DATABASE')

cnxpool = mysql.connector.pooling.MySQLConnectionPool(pool_name="mypool",
                                                      pool_size=5,
                                                      pool_reset_session=True,
                                                      host=host,
                                                      database=database,
                                                      user=user,
                                                      password=password)


def get_connection():
    connection = cnxpool.get_connection()
    connection.autocommit = True
    return connection

