from sqlalchemy import create_engine
import os

def get_database():
    """
    Returns the DisasterResponse database.
    """
    database_location = os.path.join(os.path.dirname(os.path.realpath(__file__)), "DisasterResponse.db")
    return create_engine(f'sqlite:///{database_location}')

