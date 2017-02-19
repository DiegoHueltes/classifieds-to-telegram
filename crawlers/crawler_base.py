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
        :return: [Post]
        """
        if not last_posts:
            return []
        ids_by_web_type = session.query(Post).filter(Post.web_type == self.web_page.web_type)
        last_posts_ids = [x.id for x in last_posts]
        already_tracked = ids_by_web_type.filter(Post.id.in_(last_posts_ids)).all()
        tracked_ids = {x.id for x in already_tracked}
        return [x for x in last_posts if x.id not in tracked_ids]

    def store_posts(self, posts, chat_id=None, status=None):
        """
        Save the posts passed as parameter
        :param posts: iterator of posts usually [Post]
        :param chat_id: chat id where to send this post
        :param status: status to set to all the posts
        :return [Post]
        """
        for p in posts:
            p.web_type = self.web_type
            p.to_send_id = p.to_send_id or chat_id
            if status:
                p.status = status
        return self.save_posts(posts)

    @staticmethod
    def save_posts(posts):
        try:
            session.add_all(posts)
            session.commit()
        except IntegrityError:
            traceback.print_exc()
            session.rollback()
        return posts

    @staticmethod
    def get_post_to_send():
        """
        Get the posts to be sent
        :return: [Post]
        """
        return session.query(Post).filter(Post.status != 'SENT').all()

    def save_last_updates(self, chat_id):
        """
        Fetch the last posts in the crawler, check if some of them are new, store if there are
         some new and return the new ones
        :return: [Post]
        """
        self.last_posts = self.get_last_posts()
        self.new_posts = self.get_new_posts(self.last_posts)
        if self.new_posts:
            return self.store_posts(self.new_posts, chat_id, 'SAVED')
        return []

    @staticmethod
    def text(element) -> str:
        """
        Extracts the text from the BeautifulSoup element safety or return ''
        :param element: BeutifulSoup element
        :return: BaseString
        """
        return element.text if element and hasattr(element, 'text') else ''
