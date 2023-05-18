from queue import Queue
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import os
import sys
from config import ConfigDB
from models import Url
import threading
import logging
from datetime import datetime
import requests
import time



# log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log/url_extractor.log')
# logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_html(url):
    
    try:
        response = requests.get(url)
        if response.status_code==200:
            soup = BeautifulSoup(response.content,"html.parser")
            return soup   
    except Exception as e:
        print(f"Error: {e}")
        return None
    

def get_urls(url, soup):
    urls = set()  
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
    queue = Queue() 
    queue.put(url)
    visited.add(url)
    
    db = None
    try:
        db = ConfigDB().db_connector()
    except Exception as err:
        logging.error(f"Failed to establish database connection: {err}")
        return

    while not queue.empty():
          
        url = queue.get()
  
        try:
            inpt_stmt = Url(url=url)
            db.add(inpt_stmt)
            db.commit()
            print(f"Added url: {url}")
        except Exception as err:
            print(f"Failed to add URL to database: {err}")

        soup = get_html(url)
        
        
        if soup is not None:
            urls = get_urls(url, soup)
            
            for u in urls:
                if u not in visited:
                    queue.put(u)
                    visited.add(u)
                    
    if db is not None:
        db.close()

urls_to_crawl = [ 'https://www.manoramaonline.com/','https://www.asianetnews.com','https://www.mathrubhumi.com',]

def main():
    # pid = str(os.getpid())
    # pidfile = "/tmp/url_extractor.pid"

    # if os.path.isfile(pidfile):
        
    #     sys.exit()
        
    # with open(pidfile, 'w') as f:
    #     f.write(pid)

    try:
        threads = []
        for url in urls_to_crawl:
            time.sleep(10)
            thread = threading.Thread(target=crawl_website, args=(url,))
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()
    except Exception as err:
        print(err)
        # os.unlink(pidfile)
    finally:
        print("ji")
        # os.unlink(pidfile)

main()
