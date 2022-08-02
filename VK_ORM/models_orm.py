import sqlalchemy as sq
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    user_id = sq.Column(sq.Integer, primary_key=True)
    id = sq.Column(sq.Integer, unique=True, nullable=False)

    def __str__(self):
        return f'{self.user_id = }, {self.id = }'

class Like_list(Base):
    __tablename__ = 'like_list'
    like_id = sq.Column(sq.Integer, primary_key=True)
    user_name = sq.Column(sq.String(length=40), nullable=False)
    link = sq.Column(sq.String(length=40), nullable=False)
    id = sq.Column(sq.Integer, sq.ForeignKey('users.id'), nullable=False)
    users = relationship(Users, backref='like_list')

    def __str__(self):
        return f'{self.user_name = }, {self.link = }, {self.id = }'


class Black_list(Base):
    __tablename__ = 'black_list'
    black_id = sq.Column(sq.Integer, primary_key=True)
    user_name = sq.Column(sq.String(length=40), nullable=False)
    link = sq.Column(sq.String(length=40), nullable=False)
    id = sq.Column(sq.Integer, sq.ForeignKey('users.id'), nullable=False)
    users = relationship(Users, backref='black_list')

    def __str__(self):
        return f'{self.user_name = }, {self.link = }, {self.id = }'

def create_tables(engine):
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

def insert_into_black_list(session, user_name, link, id):
    black = Black_list(user_name=user_name, link=link, id=id)
    session.add(black)
    session.commit()

def insert_into_like_list(session, user_name, link, id):
    like = Like_list(user_name=user_name, link=link, id=id)
    session.add(like)
    session.commit()

def insert_into_users(session, id):
    user = Users(id=id)
    session.add(user)
    session.commit()