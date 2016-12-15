from db.models import Post
from db.models import WebPage
from db.models import session

from db.models import engine


def init_db():
    Post.metadata.create_all(engine)
    WebPage.metadata.create_all(engine)


def get_or_create(model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


if __name__ == '__main__':
    init_db()
