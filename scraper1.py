
from bs4 import BeautifulSoup
from url_utils import crawl_website
from proxy_utils import  proxy_request
import base64
import urllib.request
import requests
import mysql.connector
from dotenv import load_dotenv
import os


load_dotenv()


host = os.environ.get('MYSQL_HOST')
user = os.environ.get('MYSQL_USER')
password = os.environ.get('MYSQL_PASSWORD')
database = os.environ.get('MYSQL_DATABASE')


conn = mysql.connector.connect(
    user=user,
    password=password,
    host=host,
    database=database   
)

# Creating a cursor object
cursor = conn.cursor()


url = 'https://www.asianetnews.com'
crawl_website(url)



def article_extractor():
    cursor.execute("SELECT url FROM urls")
    urls = [row[0] for row in cursor.fetchall()]
    if url.startswith(url):
        for url in urls:
            try:
                response = requests.get(url,timeout=10)
                # Send a GET request to the URL and parse the HTML content
                # response = proxy_request(url)
                soup = BeautifulSoup(response.content, 'html.parser')

                title = soup.find('h1').text

                # Summary = soup.find('div', {'class': 'web-summary'})
                # Summary = Summary.find('p').text

                image_div = soup.find("img", {"class": "pure-img lozad"})
                image_url = image_div.get("data-src")
                # image = urllib.request.urlopen(image_url).read()
                # image_base64 = base64.b64encode(image)

                # find the div with classname PostBody
                content_div = soup.find('div', {'class': 'PostBody'})

                # find all p tags within the post_body_div
                p_tags = content_div.find_all('p')

                content = []
                # iterate over the p tags and append their contents to the content list
                for p in p_tags:
                    content.append(p.text)
                content = ' '.join(content)


            
                sql = "INSERT INTO news (heading, content, image_url) VALUES (%s, %s, %s)"
                val = (title, content, image_url)

                cursor.execute(sql, val)

                conn.commit()

               
                
            except:
                
                continue
            
            delete_sql = "DELETE FROM urls WHERE url = %s"
            cursor.execute(delete_sql, (url,))
            conn.commit()
    else:
        continue
article_extractor()
        
        

    



cursor.close()
conn.close()

