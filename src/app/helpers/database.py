from sqlalchemy import create_engine

def get_database_engine():
    return create_engine('sqlite:///ml/data/DisasterResponse.db')

