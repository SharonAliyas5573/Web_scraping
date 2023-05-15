import sys
import os
from typing import Dict, Union, List
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts')))
from config import ConfigDB ,Session
from fastapi import FastAPI, Form
from models import News, Url
import subprocess


app = FastAPI()


def is_running(script_name: str) -> Dict[str, Union[str, bool]]:
    pidfile = f"/tmp/{script_name}.pid"
    return {"name": script_name, "status": os.path.isfile(pidfile)}





@app.get("/web/search/{query}", response_model=List[News])
async def search(query: str) -> List[News]:
    # create session
    session = Session()
    # query for matching records in heading, content and id columns
    results = session.query(News).filter(
        (News.heading.like(f"%{query}%")) |
        (News.content.like(f"%{query}%")) |
        (News.id.like(f"%{query}%"))
    ).all()
    # close session
    session.close()
    # return list of news objects
    return results


@app.get("/web/status")
def status():
    scripts = ["manorama_scraper", "url_extractor",
               "asianet_scraper", "mathrubhumi_scraper"]
    status_list = [is_running(script) for script in scripts]
    db = False
    if ConfigDB().db_connector():
        db = True
    return {"scripts": status_list, "DB_status": db}


