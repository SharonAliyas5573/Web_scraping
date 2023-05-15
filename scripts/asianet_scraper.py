from bs4 import BeautifulSoup
import urllib.request
import os
import sys
import time
import logging
from datetime import datetime
from config import get_db
from models import Url, News
from requests_tor import RequestsTor


log_file_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'log/asianet_scraper.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
rt = RequestsTor(tor_ports=(9050,), tor_cport=9051)

global main_url
main_url = 'https://www.asianetnews.com'


def article_extractor():
    print("started asianet_scraper")
    db = get_db()
    print(db)
    urls = db.query(Url.url).all()

    for url in urls:
        c_url = url.url
        if c_url.startswith(main_url):
            try:
                logging.info(f"Processing url: {c_url}")
                response = rt.get(c_url)

                soup = BeautifulSoup(response.text, 'html.parser')

                title = soup.find('h1').text

                image_div = soup.find("img", {"class": "pure-img lozad"})
                image_url = image_div.get("data-src")

                content_div = soup.find('div', {'class': 'PostBody'})

                p_tags = content_div.find_all('p')

                content = []
                for p in p_tags:
                    content.append(p.text)
                content = ' '.join(content)

                publish_date_str = soup.find(
                    'div', {'class': 'authordate'}).text.strip()[16:]
                publish_date_str = publish_date_str[:-4]
                if "t Published" in publish_date_str:
                    publish_date_str = publish_date_str.replace(
                        "t Published ", "")

                try:
                    publish_date = datetime.strptime(
                        publish_date_str, '%b %d, %Y, %I:%M %p')
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



pid = str(os.getpid())
pidfile = "/tmp/asianet_scraper.pid"


if os.path.isfile(pidfile):
    sys.exit()


directory = os.path.dirname(pidfile)
if not os.path.exists(directory):
    os.makedirs(directory)


with open(pidfile, 'w') as f:
    f.write(pid)

try:
    while True:
        article_extractor()
except Exception as err:
    print(err)
finally:
    os.unlink(pidfile)
