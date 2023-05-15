import mysql.connector

# Connect to the database
cnx = mysql.connector.connect(
    user='sharon',
    password='password',
    host='localhost',
    port='3308',
    database='web_scrape'
)

# Create a cursor object to interact with the database
cursor = cnx.cursor()

# Create a test table
create_table_query = '''
CREATE TABLE IF NOT EXISTS test_table (
    id INT PRIMARY KEY,
    name VARCHAR(50)
)
'''
cursor.execute(create_table_query)

# Insert some dummy data into the test table
insert_data_query = '''
INSERT INTO test_table (id, name)
VALUES (%s, %s)
'''
data = [(1, 'Alice'), (2, 'Bob'), (3, 'Charlie')]
cursor.executemany(insert_data_query, data)

# Commit the changes to the database
cnx.commit()

# Close the database connection
cursor.close()
cnx.close()
