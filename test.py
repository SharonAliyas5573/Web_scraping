from bs4 import BeautifulSoup
import requests
import urllib.request

url = 'https://www.mathrubhumi.com/lifestyle/fashion/actor-mamitha-baiju-new-photoshoot-in-red-saree-1.8485113?cx_testId=1&cx_testVariant=cx_1&cx_artPos=1&cx_experienceId=EX2RLNFUCLSY#cxrecs_s'


response = requests.get(url,timeout=10)

# response = proxy_request(url)
soup = BeautifulSoup(response.content, 'html.parser')

title = soup.find('h1').text

content_div = soup.find('div', {'class': 'article_contents'})

# find all p tags within the post_body_div
p_tags = content_div.find_all('p')

content = []
# iterate over the p tags and append their contents to the content list
for p in p_tags:
    content.append(p.text)
content = ' '.join(content)

image_div = soup.find("div", {"class": "article_topImg"}).find("div", {"class": "position-relative"})
image_url = urllib.parse.urljoin(url, image_div.find("img", {"class": "img-fluid"}).get("src"))

