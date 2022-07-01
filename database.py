from sqlalchemy.sql.expression import func
from alchemy import Account, Follower
from json import load

from sqlalchemy import create_engine, or_
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

with open("seguidores_politicos/config.json") as jsonfile:
    db_config = load(jsonfile)['database']

engine = create_engine(URL.create(db_config['drivername'], db_config['username'], db_config['password'], db_config['host'],
                                  db_config['port'], db_config['database']))



def upsert_account(account_tw):
    Session = sessionmaker(bind=engine)
    session = Session()

    old_account = session.query(Account).filter(Account.account_id.contains(account_tw.id)).first()

    if (old_account):
        old_account.followers_count = account_tw.public_metrics['followers_count']
    else:
        new_account = Account(
            account_id = account_tw.id,
            screen_name = account_tw.username,
            name =  account_tw.name,
            followers_count = account_tw.public_metrics['followers_count']
        )
        session.add(new_account)
        session.flush()

    session.commit()
    session.close()

def get_random_follower(qty):
    Session = sessionmaker(bind=engine)
    session = Session()

    accounts = session.query(Follower).filter(Follower.score_cap == None).order_by(func.rand()).limit(qty).all()

    session.close()
    return accounts



def get_accounts():
    Session = sessionmaker(bind=engine)
    session = Session()

    accounts = session.query(Account).all()

    session.close()
    return accounts


def get_account_details(candidate):
    Session = sessionmaker(bind=engine)
    session = Session()

    account = session.query(Account).filter_by(id=candidate).first()

    session.close()
    return account



def insert_follower_list(follower_list, account_db):  
    Session = sessionmaker(bind=engine)
    session = Session()

    for follower in follower_list:
        new_follower = Follower(
            follows = account_db.id,
            user_id = follower.id,
            screen_name = follower.username,
            created_at = follower.created_at
        )

        session.add(new_follower)

    session.commit()
    session.close()

def insert_follower_list_id(follower_list, account_db):  
    Session = sessionmaker(bind=engine)
    session = Session()

    for id in follower_list:
        new_follower = Follower(
            follows = account_db.id,
            user_id = id,
        )

        session.add(new_follower)

    session.commit()
    session.close()

def get_followers():
    Session = sessionmaker(bind=engine)
    session = Session()

    accounts = session.query(Follower).filter(Follower.created_at == None).filter(Follower.redacted == False).limit(100).all()

    session.close()
    return accounts

def update_users(user_list):  
    Session = sessionmaker(bind=engine)
    session = Session()

    for user in user_list.data:
        print(user.username)
        user_db = session.query(Follower).filter(Follower.user_id == user.id).filter(Follower.created_at == None).first()
        user_db.created_at = user.created_at
        user_db.screen_name = user.username
        
        session.add(user_db)
    for user in user_list.errors:
        print(user['value'])
        user_db = session.query(Follower).filter(Follower.user_id == user['value']).filter(Follower.redacted == False).first()
        user_db.redacted = True
        
        session.add(user_db)


    session.commit()
    session.close()

def update_score(score, user):  
    Session = sessionmaker(bind=engine)
    session = Session()

    user_db = session.query(Follower).filter(Follower.id == user.id).first()

    user_db.score_cap = score['cap']['universal']
    user_db.score_other = score['cap']['english']
    
    session.add(user_db)
    session.commit()
    session.close()
