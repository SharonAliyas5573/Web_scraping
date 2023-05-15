from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import News


class ConfigDB:
    '''
    This class is used to validate database connectivity and
    create a database session. if database connectivity is not valid
    return db as None
    '''
    
    db = None
    
    def __init__(self):
        try:
            engine.connect()
            Base.metadata.create_all(bind=engine)
            self.db: Session = SessionLocal()
        except OperationalError as e:
            pass

    def db_connector(self):
        return self.db
