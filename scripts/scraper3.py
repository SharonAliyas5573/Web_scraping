from bs4 import BeautifulSoup
# from proxy_utils import proxy_request
# import base64
import urllib.request
import requests
import mysql.connector.pooling
from dotenv import load_dotenv
import os
import logging

from datetime import datetime

from db_pool import get_connection

# from scripts.db_pool import get_connection

load_dotenv()

host = os.environ.get('MYSQL_HOST')
user = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
database = os.environ.get('MYSQL_DATABASE')


cnxpool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="mypool",
    pool_size=5,
    pool_reset_session=True,
    host=host,
    database=database,
    user=user,
    password=password
)


log_file_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'crawler3.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


global main_url
main_url = 'https://www.manoramaonline.com/'


def article_extractor():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT url FROM urls")
    urls = [row[0] for row in cursor.fetchall()]


    for url in urls:
        if url.startswith(main_url):
            try:
                # logging.info(f"Processing url: {url}")
                response = requests.get(url, timeout=10)
                # Send a GET request to the URL and parse the HTML content
                # response = proxy_request(url)
                soup = BeautifulSoup(response.content, 'html.parser')

                title = soup.find('h1', {'class': 'story-headline'}).text

                image_tag = soup.select_one(
                    'div.image.parbase.section figure.story-figure div.story-figure-image img')
                image_url = image_tag['data-src-web']

                content_div = soup.find(
                    'div', {'class': 'article rte-article'})

                p_tags = content_div.find_all('p')
                content = []

                for p in p_tags:
                    content.append(p.text)
                content = ' '.join(content)

                time_string = soup.find(
                    'time', {'class': 'story-author-date'}).text
                time_format = "%B %d, %Y %I:%M %p %Z"
                publish_date = datetime.strptime(time_string, time_format)

                source_tag = "Manoarama"

                sql = "INSERT INTO news (heading, content, image_url,publish_date,source_tag) VALUES (%s, %s, %s,%s,%s)"
                val = (title, content, image_url,publish_date,source_tag)

                

                cursor.execute(sql, val)
                connection.commit()
                logging.info(f"Inserted article with title: {title}")

            except Exception as e:
                logging.error(f"Error processing url {url}: {e}")
                continue

            # delete_sql = "DELETE FROM urls WHERE url = %s"
            # cursor.execute(delete_sql, (url,))
            # connection.commit()
            # logging.info(f"Deleted processed url: {url}")

        else:
            logging.warning(
                f"Skipping url {url} as it does not match main_url {main_url}")
            continue

    cursor.close()
    connection.close()


article_extractor()
