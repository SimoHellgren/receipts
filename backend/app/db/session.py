import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


load_dotenv()

DB_VAR = 'DEV_DB_URI' if os.getenv('MODE') == 'DEV' else 'DB_URI'

engine = create_engine(os.getenv(DB_VAR))

SessionLocal = sessionmaker(bind=engine)
