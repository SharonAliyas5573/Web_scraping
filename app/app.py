import sys
import os
from typing import Dict, Union, List
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
from config import get_db
from sqlalchemy import text ,or_
from fastapi import FastAPI, Response
from models import News, Url
from config import get_db
import subprocess
from datetime import datetime
import redis
from fastapi.responses import JSONResponse

app = FastAPI()

redis_host = 'redis'  # Use the service name as the hostname since both containers are in the same Docker network
redis_port = 6379  # Default Redis port

redis_client = redis.Redis(host=redis_host, port=redis_port)

scraping_scripts = {
    "scraper-1": "Asianet scraper",
    "scraper-2": "Manorama Scraper",
    "scraper-3": "Mathrubhumi scraper"
}

@app.get("/web/status")
def get_scraping_status():
    db_status = get_db()
    
    status = {
        "database": "running" if db_status else "stopped",
    }
    
    for name, display_name in scraping_scripts.items():
        script_status = redis_client.get(name)
        if script_status is None:
            status[display_name] = "unknown"
        else:
            status[display_name] = script_status.decode()

    return JSONResponse(content=status, status_code=200)


@app.get("/web/search")
def search(q:str =None,source_tag: str = None, publish_date: str = None , publish_date_range: str = None):
    db = get_db()
    query = db.query(News)
    if q:
        query= db.query(News).filter(or_(News.heading.ilike('%'+q+'%'), News.content.ilike('%'+q+'%')))

    if source_tag:
        query = query.filter(News.source_tag.ilike('%'+source_tag+'%'))

    if publish_date:
        publish_date = datetime.strptime(publish_date, '%Y-%m-%d').date()
        query = query.filter(News.publish_date == publish_date)

    if publish_date_range:
        start_date, end_date = publish_date_range.split(',')
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        query = query.filter(News.publish_date.between(start_date, end_date))

    results = query.all()
    return results
     

@app.get("/web/all")
def all():
    db = get_db()
    news = db.query(News).all()
    return news







