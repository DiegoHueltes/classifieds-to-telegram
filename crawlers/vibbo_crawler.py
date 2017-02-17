# coding=utf-8


import requests
from bs4 import BeautifulSoup

from crawlers.crawler_base import Crawler
from db.models import Post


class VibboCrawler(Crawler):
    """
    Crawler specific to gather the information from the web www.vibbo.com old segundamano.es
    """
    crawler_url = 'https://www.vibbo.com'
    web_type = 'VIBBO'

    def __init__(self, target_url, *args, **kwargs):
        super(VibboCrawler, self).__init__(*args, **kwargs)
        self.target_url = target_url

    def get_last_posts(self):
        """
        Specific implementation of the generic get_last_posts to gather the last
        post in the web
        :return: [Post]
        """
        last_posts = []
        r = requests.get(self.target_url)
        html = BeautifulSoup(r.content, 'html.parser')
        raw_posts = html.findAll("div", {"class": "list_ads_row"})

        for post in raw_posts:
            title_element = post.find("a", {"class": "subjectTitle"})
            title = cleaning_spaces(self.text(title_element))
            href = title_element['href']
            description = ' -- '.join(map(self.text, [post.find("p", {"class": "zone"}),
                                                      post.find("p", {"class": "date"})]))
            id_post = int(post['id'])
            price_full = cleaning_spaces(self.text(post.find("a", {"class": "subjectPrice"})))
            price = int(price_full[:-1].replace('.', ''))  # Removing currency symbol
            image_element = post.find('img', {'class': 'lazy'})
            image_src = None
            if image_element:
                image_src = image_element.get('title', '')
            complete_href = href
            description = '\n'.join([title, price_full, cleaning_spaces(description), complete_href])
            last_posts.append(Post(id=id_post, href=complete_href, description=description, image=image_src,
                                   price=price))
        return last_posts


def cleaning_spaces(txt):
    return ' '.join(txt.split())
