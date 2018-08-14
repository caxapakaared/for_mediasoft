from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from app import db
from config import db_uri


engine = create_engine(db_uri)
if not database_exists(engine.url):
    create_database(engine.url)

db.create_all()