import redis
import os
import time
import logging
from datetime import datetime
from config import get_db
from models import Url, News
import requests

redis_host = 'redis'  # Use the service name as the hostname since both containers are in the same Docker network
redis_port = 6379  # Default Redis port

redis_client = redis.Redis(host=redis_host, port=redis_port)


def set_scraping_status(name, status):
    redis_client.set(name, status)


log_file_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'log/manoarama_scraper.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


global main_url
main_url = 'https://www.manoramaonline.com/'


def perform_web_scraping():

    try:
        db = get_db()
        urls = db.query(Url.url).all()
        print("db is ok")
        for url in urls:
            c_url = url.url
            if c_url.startswith(main_url):
                try:
                    logging.info(f"Processing url: {url}")
                    response = requests.get(c_url)
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
                    try:
                        time_string = soup.find(
                            'time', {'class': 'story-author-date'}).text
                        time_format = "%B %d, %Y %I:%M %p %Z"
                        publish_date = datetime.strptime(time_string, time_format)
                    except:
                        pass
                    source_tag = "Manoarama"
                    article = News(heading=title, content=content, image_url=image_url,
                                publish_date=publish_date, source_tag=source_tag)
                    db.add(article)
                    db.commit()

                    logging.info(f"Inserted article from Manorama")

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
        set_scraping_status('scraper-2', 'running')
        # perform_web_scraping()
    #     set_scraping_status('scraper-2', 'stopped')
        value = redis_client.get('scraper-2')

        # Decode the value if it's in bytes
        if value is not None:
            value = value.decode()

        # Print the value
        print(f'The value of the key "test_key" is: {value}')
    except Exception as err:
        logging.error(f"An error occurred: {err}")

    time.sleep(5)  # Sleep for 5 seconds before running the next iteration


