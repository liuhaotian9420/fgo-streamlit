# src/mysql_model.py
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class MySQLView(Base):
    __tablename__ = 'mysql_view'
    __table_args__ = {'extend_existing': True}  # Needed for views
    id = Column(Integer, primary_key=True)
    name = Column(String)
    value = Column(Float)
    timestamp = Column(DateTime)

# MySQL engine and session
mysql_engine = create_engine('mysql+pymysql://developer:VhUdQSBX8H3NmTA@118.195.250.136:14306/fgo')
MySQLSession = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)


