# src/mysql_model.py
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import streamlit as st

Base = declarative_base()

class ArtsLooper(Base):
    __tablename__ = 'arts_looper'
    __table_args__ = {'extend_existing': True}  # Needed for views
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    rarity = Column(Integer)
    class_name = Column(String(255))
    atk = Column(Integer)
    tendancy = Column(Float)
    np_rate = Column(Float)
    np_hits = Column(String(255))
    is_strengthened = Column(Boolean)
    class_mod = Column(Integer)
    attribute = Column(String(255))
    traits = Column(String(255))
    star_absorb = Column(Integer)
    star_gen = Column(Integer)
    
class ArtsLooperBuffs(Base):
    
    __tablename__ = 'arts_looper_buffs'
    __table_args__ = {'extend_existing': True}  # Needed for views
    servant_id = Column(Integer,primary_key=True)
    servant_name = Column(String(255))
    skill_type  = Column(String(255),primary_key=True)
    skill_no = Column(Integer,primary_key=True)
    buff_name = Column(String(255),primary_key=True)
    buff_type = Column(String(255))
    function_target_type = Column(String(255),primary_key=True)
    function_type = Column(String(255),primary_key=True)
    function_target_traits = Column(String(255))
    value = Column(Integer,primary_key=True)
    count = Column(Integer)
    turn = Column(Integer)
    rate = Column(Integer)
    userate = Column(Integer)
    
class ArtsMetaSupport(Base):
    
    __tablename__ = 'arts_meta_support'
    __table_args__ = {'extend_existing': True}  # Needed for views
    servant_id = Column(Integer,primary_key=True)
    servant_name = Column(String(255))
    skill_type  = Column(String(255),primary_key=True)
    skill_no = Column(Integer,primary_key=True)
    buff_name = Column(String(255),primary_key=True)
    buff_type = Column(String(255))
    function_target_type = Column(String(255),primary_key=True)
    function_type = Column(String(255),primary_key=True)
    function_target_traits = Column(String(255))
    value = Column(Integer,primary_key=True)
    count = Column(Integer)
    turn = Column(Integer)
    rate = Column(Integer)
    userate = Column(Integer)
    
class ArtsCraftEssence(Base):
    
    __tablename__ = 'arts_craft_essence'
    __table_args__ = {'extend_existing': True}  # Needed for views
    ce_id = Column(Integer, primary_key=True)
    ce_name = Column(String(255))
    buff_name = Column(String(255))
    buff_type = Column(String(255))
    value = Column(Integer)
    turn = Column(Integer)
    cost = Column(Integer)
    max_atk = Column(Integer)
    
    
# MySQL engine and session
username = st.secrets.mysql_secrets.username
password = st.secrets.mysql_secrets.password
host = st.secrets.mysql_secrets.host
port = st.secrets.mysql_secrets.port
database = st.secrets.mysql_secrets.database
mysql_engine = create_engine(f'mysql+pymysql://{username}:{password}@{host}:{port}/{database}', echo=False)
MySQLSession = sessionmaker(autocommit=False, autoflush=False, bind=mysql_engine)

