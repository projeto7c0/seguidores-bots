from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key = True)
    account_id = Column(Text)
    screen_name = Column(Text)
    name = Column(Text)
    followers_count = Column(Integer)
    bearer_token = Column(Text)



class Follower(Base):
    __tablename__ = 'followers'

    id = Column(Integer, primary_key = True)
    user_id = Column(Text)
    follows = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    screen_name = Column(Text)
    created_at = Column(DateTime)
    redacted = Column(Boolean)
    score_cap = Column(Float)
    score_other = Column(Float)
    score_other2 = Column(Float)

    def __repr__(self):
        return f'Follower {self.user_id}'