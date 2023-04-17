import threading
from queue import Queue
from urllib.parse import urljoin
import requests
import time
from proxy_utils import proxy_request 
from bs4 import BeautifulSoup

url = 'https://www.asianetnews.com'
visited = set()  # set to store visited pages
queue = Queue()  # queue to store urls to visit


def get_html(url):
    try:
        response = proxy_request(url)
        # response = requests.get(url, timeout=5)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            return soup
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
    return None


def get_urls(soup):
    urls = set()  # set to store unique urls on current page
    for link in soup.find_all('a'):
        href = link.get('href')
        if href and href.startswith('/'):
            urls.add(urljoin(url, href))

    return urls


def worker():
    while True:
        url = queue.get()
        if url in visited:
            queue.task_done()
            continue
        visited.add(url)
        soup = get_html(url)
        if soup is not None:
            urls = get_urls(soup)
            for u in urls:
                queue.put(u)
            
        queue.task_done()


def main():
    start_time = time.time()
    queue.put(url)

    # create worker threads
    for i in range(8):
        t = threading.Thread(target=worker)
        t.daemon = True
        t.start()

    # wait for all urls to be visited
    queue.join()
    print(f"{len(visited)} pages visited in {time.time() - start_time:.2f} seconds")


if __name__ == '__main__':
    main()
