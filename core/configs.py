from pydantic import BaseSettings
from sqlalchemy.ext.declarative import declarative_base

class Settings(BaseSettings):
    DB_URL: str = "postgresql+psycopg2://{}:postgres@pgsql.{}.com:5432/{}"
    #DB_URL: str = "ibm_db_sa+pyodbc400://{username}:{password}@{host}:{port}/{database};currentSchema={schema}"
    DBBaseModel= declarative_base()
    
    class Config:
        case_sensitive = True
                
                
settings = Settings()