import subprocess
from threading import Thread
import sys
def run_file(filename):
  p1 = subprocess.Popen([sys.executable, filename])
  p1.communicate()

t1 = Thread(target=lambda:run_file("mathrubhumi_scraper.py"))
t2 = Thread(target=lambda:run_file("manorama_scraper.py"))
t3 = Thread(target=lambda:run_file("asianet_scraper.py"))
t4 = Thread(target=lambda:run_file("url_extractor.py"))
t5 = Thread(target=lambda:run_file("db_dumb.py"))

t1.start()
t2.start()
# t3.start()
# t4.start()
# t5.start()