from bs4 import BeautifulSoup
# from proxy_utils import  proxy_request
# import base64
import urllib.request
import requests
from db_pool import get_connection
from dotenv import load_dotenv
import os
import logging
from datetime import datetime
import mysql.connector.pooling


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


logging.basicConfig(filename='crawler2.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

global main_url
main_url = 'https://www.mathrubhumi.com'


def article_extractor():
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT url FROM urls")
        urls = [row[0] for row in cursor.fetchall()]

        for url in urls:
            if url.startswith(main_url):
                try:
                    response = requests.get(url, timeout=10)

                    # response = proxy_request(url)
                    soup = BeautifulSoup(response.content, 'html.parser')

                    title = soup.find('h1').text

                    content_div = soup.find(
                        'div', {'class': 'article_contents'})

                    # find all p tags within the post_body_div
                    p_tags = content_div.find_all('p')

                    content = []
                    # iterate over the p tags and append their contents to the content list
                    for p in p_tags:
                        content.append(p.text)
                    content = ' '.join(content)

                    image_div = soup.find("div", {"class": "article_topImg"}).find(
                        "div", {"class": "position-relative"})
                    image_url = urllib.parse.urljoin(url, image_div.find(
                        "img", {"class": "img-fluid"}).get("src"))

                    publish_date_div = soup.find(
                        'div', {'class': 'mpp-story-column-profile-desc'}).find('time')
                    publish_date = datetime.fromisoformat(
                        publish_date_div['datetime'][:-6]).strftime('%Y-%m-%d %H:%M:%S')

                    source_tag = "Mathrubhumi"

                    sql = "INSERT INTO news (heading, content, image_url,publish_date,source_tag) VALUES (%s, %s, %s,%s,%s)"
                    val = (title, content, image_url, publish_date, source_tag)

                    cursor.execute(sql, val)
                    conn.commit()

                    logging.info(f"Inserted article with title: {title}")

                except Exception as e:
                    conn.rollback()
                    logging.error(f"Error processing url {url}: {e}")

                # delete_sql = "DELETE FROM urls WHERE url = %s"
                # cursor.execute(delete_sql, (url,))
                # conn.commit()
                # logging.info(f"Deleted processed url: {url}")

            else:
                logging.warning(
                    f"Skipping url {url} as it does not match main_url {main_url}")

    except Exception as e:
        logging.error(f"Error connecting to MySQL database: {e}")

    finally:
        if 'conn' in locals() and conn.is_connected():
            cursor.close()
            conn.close()
            logging.info("MySQL connection closed")


article_extractor()
