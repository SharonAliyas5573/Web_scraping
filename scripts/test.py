from sqlalchemy.orm import Session
from config import get_db
from models import Url


def test_insert_url():
    # Get a database session
    db: Session = get_db()

    # Create a new URL object
    url = Url(url="http://example.com")

    # Add the URL to the session and commit it to the database
    db.add(url)
    db.commit()

    # Close the session
    db.close()


if __name__ == '__main__':
    test_insert_url()
    print("Test successful!")
