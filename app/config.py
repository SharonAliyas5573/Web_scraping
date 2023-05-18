from sqlalchemy.orm import Session
from database import SessionLocal, engine, Base
from sqlalchemy.exc import OperationalError
import time


class ConfigDB:
    """
    This class is used to validate database connectivity and
    create a database session. If database connectivity is not valid
    return db as None.
    """
    db = None

    def __init__(self):
        while self.db is None:
            try:
                engine.connect()
                Base.metadata.create_all(bind=engine)
                self.db: Session = SessionLocal()
            except OperationalError as e:
                print(f"Error connecting to database: {str(e)}")
                time.sleep(2)

    def db_connector(self):
        return self.db


def get_db():
    return ConfigDB().db_connector()
