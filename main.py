from newspaper import Config, Article, fulltext
from newspaper import build
import mysql.connector


config = Config()
config.request_timeout = 10
config.memoize_articles = False 

mydb = mysql.connector.connect(
  host="localhost",
  user="sharon",
  password="Sharon@2004",
  database="mydatabase"
)


url = 'https://www.asianetnews.com/latest-news'



paper = build(url, config=config)


article_urls=[]
for article in paper.articles:
    try:
        article.download()
        article.parse()
        article.nlp()
        article_urls.append(article.url)
        

        url = article.url
        heading = article.title
        
        insert_stmt = "INSERT INTO my_table (url, heading) VALUES (%s, %s)"
        mycursor = mydb.cursor()
        data = (url, heading)
        print("Insert statement:", insert_stmt)
       
        mydb.commit()



        print(article.title)
        
    except:
        print("An error occurred ")

mycursor.close()
mydb.close()