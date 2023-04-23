from queue import Queue
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from proxy_utils import proxy_request
import mysql.connector
from dotenv import load_dotenv
import os
from db_pool import get_connection
import threading


load_dotenv()


host = os.environ.get('MYSQL_HOST')
user = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
database = os.environ.get('MYSQL_DATABASE')


conn = mysql.connector.connect(
    user=user,
    password=password,
    host=host,
    database=database   
)


# Creating a cursor object
cursor = conn.cursor()


def get_html(url):
    try:
        # response = proxy_request(url)
        response = requests.get(url, timeout=50)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            return soup
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    return None

def get_urls(url, soup):
    urls = set()  # set to store unique urls on current page
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and (href.startswith('/') or href.startswith(url)):
            if href.startswith(url):
                urls.add(href)
            else:
                urls.add(urljoin(url, href))
    return urls



def crawl_website(url):
    visited = set()  # set to store visited pages
    queue = Queue()  # queue to store urls to visit
    queue.put(url)
    visited.add(url)

    connection = get_connection()

    while not queue.empty():
        url = queue.get()
        # Add URL to database
        try:
            cursor = connection.cursor()
            cursor.execute("INSERT INTO urls (url) VALUES (%s)", (url,))
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
        connection.commit()

        soup = get_html(url)
        if soup is not None:
            urls = get_urls(url, soup)
            for u in urls:
                if u not in visited:
                    queue.put(u)
                    visited.add(u)



    connection.close()

urls_to_crawl = [ 'https://www.manoramaonline.com/','https://www.asianetnews.com','https://www.mathrubhumi.com',]



threads = []
for url in urls_to_crawl:
    thread = threading.Thread(target=crawl_website, args=(url,))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

cursor.close()
conn.close()