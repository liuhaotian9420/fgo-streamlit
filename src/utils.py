import os
from urllib.parse import urlparse
import json

from sqlalchemy import create_engine, inspect,func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from functools import wraps
from collections import defaultdict
from .model import Base,sqlite_session

def sqlite_operation(messages=None):
    if messages is None:
        messages = {}
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            session = sqlite_session()
            try:
                result = func(session, *args, **kwargs)
                session.commit()
                return result
            except SQLAlchemyError as e:
                session.rollback()
                error_type = type(e).__name__
                custom_message = messages.get(error_type, f"Error in {func.__name__}")
                raise Exception(f"{custom_message}: {str(e)}") from e
            finally:
                session.close()
        return wrapper
    return decorator


def check_cache(url,cache_dir='cache'):
    parsed_url = urlparse(url)
    filename = '_'.join(parsed_url.path.split('/'))
    if os.path.isfile(os.path.join(cache_dir,filename+'.json')):
        with open(os.path.join(cache_dir,filename+'.json'),'r') as f:
            return json.load(f)
    else:
        return None
    
def add_cache(data,url,cache_dir='cache'):
    parsed_url = urlparse(url)
    filename = '_'.join(parsed_url.path.split('/'))
    with open(os.path.join(cache_dir,filename+'.json'),'w') as f:
        json.dump(data,f,indent=4)
        
def reverse_mapping(data:dict)->dict:
    return {v: k for k, v in data.items()}