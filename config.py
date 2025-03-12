from dataclasses import dataclass
from environs import Env

@dataclass
class Database:
    authors_database_url: str
    logging_database_url: str
    
@dataclass
class Config:
    database: Database
    
def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        database=Database(
            authors_database_url=env('AUTHORS_DATABASE_URL'),
            logging_database_url=env('LOGGING_DATABASE_URL')
        )
    )