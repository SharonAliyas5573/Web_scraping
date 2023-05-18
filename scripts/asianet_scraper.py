import redis
import time
import logging
import os
from datetime import datetime
from config import get_db
from models import Url, News
import requests

redis_host = 'redis'  # Use the service name as the hostname since both containers are in the same Docker network
redis_port = 6379  # Default Redis port

redis_client = redis.Redis(host=redis_host, port=redis_port)


def set_scraping_status(name, status):
    redis_client.set(name, status)


log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log/asianet_scraper.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


global main_url
main_url = 'https://www.asianetnews.com'


def perform_web_scraping():
    try:
        db = get_db()
        urls = db.query(Url.url).all()

        for url in urls:
            c_url = url.url
            if c_url.startswith(main_url):
                try:
                    logging.info(f"Processing url: {c_url}")
                    response = requests.get(c_url)

                    soup = BeautifulSoup(response.content, 'html.parser')

                    title = soup.find('h1').text

                    image_div = soup.find("img", {"class": "pure-img lozad"})
                    image_url = image_div.get("data-src")

                    content_div = soup.find('div', {'class': 'PostBody'})

                    p_tags = content_div.find_all('p')

                    content = []
                    for p in p_tags:
                        content.append(p.text)
                    content = ' '.join(content)

                    publish_date_str = soup.find('div', {'class': 'authordate'}).text.strip()[16:]
                    publish_date_str = publish_date_str[:-4]
                    if "t Published" in publish_date_str:
                        publish_date_str = publish_date_str.replace("t Published ", "")

                    try:
                        publish_date = datetime.strptime(publish_date_str, '%b %d, %Y, %I:%M %p')
                    except ValueError as e:
                        logging.error(f"Error parsing publish date: {e}")
                        publish_date = datetime.now()

                    source_tag = "Asianet"

                    article = News(heading=title, content=content, image_url=image_url,
                                   publish_date=publish_date, source_tag=source_tag)
                    db.add(article)
                    db.commit()
                    logging.info(f"Inserted article from Asianet")

                except Exception as e:
                    logging.error(f"Error processing url {c_url}: {e}")
                    continue

            else:
                continue

        db.close()

    except Exception as err:
        logging.error(f"An error occurred while performing web scraping: {err}")


while True:
    try:
        set_scraping_status('scraper-1', 'running')
        perform_web_scraping()
        set_scraping_status('scraper-1', 'stopped')
    except Exception as err:
        logging.error(f"An error occurred: {err}")

    time.sleep(5)  # Sleep for 5 seconds before running the next iteration
