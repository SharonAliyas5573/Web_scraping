from bs4 import BeautifulSoup
import urllib.request
import requests
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from dotenv import load_dotenv
import os
import logging

from datetime import datetime

load_dotenv()

host = os.environ.get('MYSQL_HOST')
user = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
database = os.environ.get('MYSQL_DATABASE')

engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

Base = declarative_base()

class News(Base):
    __tablename__ = 'news'
    id = Column(Integer, primary_key=True, autoincrement=True)
    heading = Column(String(255))
    content = Column(String(2000))
    image_url = Column(String(255))
    publish_date = Column(DateTime)
    source_tag = Column(String(255))

Session = sessionmaker(bind=engine)

log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'crawler1.log')
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

global main_url
main_url = 'https://www.asianetnews.com'

def article_extractor():
    session = Session()

    urls=['']
    for url in urls:
        if url.startswith(main_url):
            try:
                logging.info(f"Processing url: {url}")
                response = requests.get(url, timeout=10)
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

                article = News(heading=title, content=content, image_url=image_url, publish_date=publish_date, source_tag=source_tag)
                session.add(article)
                session.commit()
                logging.info(f"Inserted article with title: {title}")

            except Exception as e:
                logging.error(f"Error processing url {url}: {e}")
                continue

        else:
            logging.warning(f"Skipping url {url} as it does not match main_url {main_url}")
            continue

    session.close()

while True:
    try:
        article_extractor()
    except Exception as e:
        logging.error(f"Error in article_extractor(): {e}")
        continue
