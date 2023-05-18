import redis
import time
import logging
from datetime import datetime
from config import get_db
import os
from models import Url, News
import requests

redis_host = 'redis'  # Use the service name as the hostname since both containers are in the same Docker network
redis_port = 6379  # Default Redis port

redis_client = redis.Redis(host=redis_host, port=redis_port)


def set_scraping_status(name, status):
    redis_client.set(name, status)


log_file_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'log/mathrubumi_scraper.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


global main_url
main_url = 'https://www.mathrubhumi.com'


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
                    image_url = urllib.parse.urljoin(c_url, image_div.find(
                        "img", {"class": "img-fluid"}).get("src"))

                    publish_date_div = soup.find(
                        'div', {'class': 'mpp-story-column-profile-desc'}).find('time')
                    publish_date = datetime.fromisoformat(
                        publish_date_div['datetime'][:-6]).strftime('%Y-%m-%d %H:%M:%S')

                    source_tag = "Mathrubhumi"
                    article = News(heading=title, content=content, image_url=image_url,
                                publish_date=publish_date, source_tag=source_tag)
                    db.add(article)
                    db.commit()

                    logging.info(f"Inserted article from Mathrubhumi")

                except Exception as e:

                    logging.error(f"Error processing url {c_url}: {e}")

            else:
                
                continue
        db.close()
    except Exception as err:
        logging.error(f"An error occurred while performing web scraping: {err}")

while True:
    try:
        set_scraping_status('scraper-3', 'running')
        perform_web_scraping()
        set_scraping_status('scraper-3', 'stopped')
    except Exception as err:
        logging.error(f"An error occurred: {err}")

    time.sleep(5)  # Sleep for 5 seconds before running the next iteration




