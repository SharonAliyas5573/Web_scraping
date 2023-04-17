# __Program Overview__

This project is a web scraper that extracts news articles from the  News website and stores them in a MySQL database.Uses the BeautifulSoup library for parsing HTML and the requests library for making HTTP requests. The scraper also uses a list of proxies to make requests to the website, in order to avoid getting blocked by the website's anti-scraping measures.

The project consists of three main Python scripts :
- __scraper.py__: This script contains the main logic for the scraper, which extracts news articles from the  News website and stores them in a MySQL database.
- __url_utils.py__: This script contains utility functions for crawling a website and extracting URLs.
- __proxy_utils.py__: This script contains utility functions for updating and using a list of proxies.


1.__url_utils.py__

- This module contains functions for crawling a website and   extracting all the URLs.

    - Functions:

        1. __get_html(url)__ - This function makes a request to a URL and returns the HTML content of the page as a BeautifulSoup object.
        2. __get_urls(url, soup)__ - This function extracts all the URLs on the page and returns them as a set.
        3. __crawl_website(url)__ - This function uses breadth-first search to crawl a website and extract all the URLs on the site. It starts by adding the base URL to a queue and then processes each URL in the queue by extracting all the URLs on that page and adding them to the queue if they haven't been visited already.

2. __proxy_utils.py__

   - This module contains functions for updating and using a list of proxies.
        - Functions

            1. __update_proxies()__ - This function makes a request to a proxy API and returns a dictionary of proxies.
            2. __proxy_request(target_url)__ - This function makes a request to a target URL using a proxy from the list of proxies. It first tries each proxy in the list until it finds one that works, and then returns the response.
3. __scraper.py__
    - This module is the main program that uses the functions from the other modules to scrape news articles from the News website.
        - Functions

            1. __article_extractor()__ - This function extracts the title, content, and image URL from each news article and inserts them into a MySQL database.

- Database Used :- MySQL
    - The MySQL database consists of two tables:

        1. __urls__ - This table stores all the URLs that have been visited during the crawling process.
        2. __news__ - This table stores the title, content, and image URL for each news article that has been extracted.


## __Installation__

1. Clone the repository

2. Change into the repository directory:
```bash
cd sample-python-project
```
3. Create a Python virtual environment:

```bash
python3 -m venv env
```
4. Activate the virtual environment:

```bash
source env/bin/activate
```
5. Install dependencies:
```py
pip install -r requirements.txt
```
6. Set up the databse 

7. To run :
```
python scraper.py
````

## __To set up databse in Docker__


1. Create an .env file with your MySQL connection credentials, following the example in the .env.example file.
2. Build the Docker image by running the following command:
``` 
docker build -t <docker-image-name> .
```
3. To run a container from the image
```
docker run --name <docker-container-name> --env-file .env -d <docker-image-name>
```
4. To stop the container:

```
docker stop  <docker-container-name>
```