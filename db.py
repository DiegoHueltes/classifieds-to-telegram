from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///posts.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True)
    href = Column(String)
    description = Column(String)
    image = Column(String)


def init_db():
    Post.metadata.create_all(engine)


if __name__ == '__main__':
    init_db()
