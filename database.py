from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from urllib.parse import quote

URL_DATABASE = 'mysql+pymysql://root:%s@localhost:3306/to_do_schema' % quote('Password')

engine = create_engine(URL_DATABASE)

LocalSession = sessionmaker(autoflush=False, autocommit=False, bind=engine)

base = declarative_base()
