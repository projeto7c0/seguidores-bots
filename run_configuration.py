from alchemy import Follower, Account
from json import load
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL


## Criando tabelas
with open("seguidores_politicos/config.json") as jsonfile:
    db_config = load(jsonfile)['database']

engine = create_engine(URL(db_config['drivername'], 
						   db_config['username'], db_config['password'], 
						   db_config['host'], db_config['port'], 
						   db_config['database']))

Account.__table__.create(bind=engine, checkfirst=True)
Follower.__table__.create(bind=engine, checkfirst=True)
