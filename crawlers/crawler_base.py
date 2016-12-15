import traceback

from sqlalchemy.exc import IntegrityError

from db import get_or_create
from db.models import session, WebPage, Post


class Crawler:
    crawler_url = None
    web_type = None

    def __init__(self, chat_id=None, *args, **kwargs):
        """
        Crawler generic interface
        :param chat_id: optional parameter to specify where the crawler should be writing the results
        """
        self.chat_id = chat_id
        self.last_posts = []
        self.new_posts = []
        self.web_page = get_or_create(WebPage, web_type=self.web_type, url=self.crawler_url)

    def get_last_posts(self):
        """
        Generic method to get the last posts of any crawler
        :return: [Post]
        """
        pass

    def get_new_posts(self, last_posts):
        """
        Checking if some of the last_posts are already in the database
        :return:
        """
        if not last_posts:
            return []
        ids_by_web_type = session.query(Post).filter(Post.web_type == self.web_page.web_type)
        last_posts_ids = [int(x.id) for x in last_posts]
        already_tracked = ids_by_web_type.filter(Post.id.in_(last_posts_ids)).all()
        tracked_ids = {x.id for x in already_tracked}
        return [x for x in last_posts if int(x.id) not in tracked_ids]

    def store_new_posts(self, posts):
        """
        Save the posts passed as parameter
        :param posts: iterator of posts usually [Post]
        """
        for p in posts:
            p.web_type = self.web_page.web_type
        session.add_all(posts)
        try:
            session.commit()
        except IntegrityError:
            traceback.print_exc()
            session.rollback()

    def get_last_updates(self):
        """
        Fetch the last posts in the crawler, check if some of them are new, store if there are
         some new and return the new ones
        :return: [posts]
        """
        self.last_posts = self.get_last_posts()
        self.new_posts = self.get_new_posts(self.last_posts)
        if self.new_posts:
            self.store_new_posts(self.new_posts)
        return self.new_posts
