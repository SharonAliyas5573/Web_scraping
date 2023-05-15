from bs4 import BeautifulSoup
import urllib.request
import os
import sys
import logging
from datetime import datetime
from config import get_db
from models import Url, News
from requests_tor import RequestsTor


log_file_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'log/manoarama_scraper.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
rt = RequestsTor(tor_ports=(9050,), tor_cport=9051)

global main_url
main_url = 'https://www.manoramaonline.com/'


def article_extractor():
    print("started manorama-scraper")
   
    db = get_db()
    urls = db.query(Url.url).all()
    print("db is ok")
    for url in urls:
        c_url = url.url
        if c_url.startswith(main_url):
            try:
                logging.info(f"Processing url: {url}")
                response = rt.get(c_url)
                soup = BeautifulSoup(response.text, 'html.parser')

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

pid = str(os.getpid())
pidfile = "/tmp/manorama_scraper.pid"


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

