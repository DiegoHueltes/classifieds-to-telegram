from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import DB_PATH

engine = create_engine('sqlite:////{}'.format(DB_PATH))
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session()


class WebPage(Base):
    __tablename__ = 'web_pages'

    web_type = Column(String, primary_key=True)
    url = Column(String)

    def __repr__(self):
        return '<WebPage(url={})>'.format(self.url)


class Post(Base):
    __tablename__ = 'posts'

    id = Column(String, primary_key=True)
    web_type = Column(String, ForeignKey('web_pages.web_type'), primary_key=True)
    href = Column(String)
    description = Column(String)
    image = Column(String)
    price = Column(Float)
    status = Column(String, nullable=False)  # possible {SAVED, SENT, ERROR}
    to_send_id = Column(Integer)  # Chat id where to send this Post

    def __repr__(self):
        title = self.description[:20] if self.description else ''
        return '<Post(price={}, title={}, href={})>'.format(self.price, title, self.href)
