from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
SQLALCHEMY_DATABASE_URL = "postgresql://hello_flask:hello_flask@db:5432/hello_flask_dev"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
Session = sessionmaker(bind=engine)

Base = declarative_base()
