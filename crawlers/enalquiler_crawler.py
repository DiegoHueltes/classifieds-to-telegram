# coding=utf-8


import requests
from bs4 import BeautifulSoup

from crawlers.crawler_base import Crawler
from db.models import Post


class EnalquilerCrawler(Crawler):
    """
    Crawler specific to gather the information from the web www.enalquiler.com
    """
    crawler_url = 'https://www.enalquiler.com'
    web_type = 'ENALQUILER'

    def __init__(self, target_url, *args, **kwargs):
        super(EnalquilerCrawler, self).__init__(*args, **kwargs)
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
        raw_posts = html.findAll("li", {"class": "property-item"})

        for post in raw_posts:
            list_position = post.get('list-position')
            if not list_position:
                continue
            title_element = post.find("a", {"class": "property-title"})
            title = cleaning_spaces(self.text(title_element))
            href = title_element['href']
            description = cleaning_spaces(self.text(post.find("div", {"class": "property-info-wrapper"})))
            id_post = str(post['list-item'])
            price_full = cleaning_spaces(self.text(post.find("div", {"class": "property-price"})))
            price = price_full[:-2]  # Removing currency symbol
            image_element = post.find('div', {'class': 'property-img-wrapper'})
            image_src = None
            if image_element:
                image_src = image_element.get('images-path', '').replace('{width}', 'se')
            complete_href = href
            description = '\n'.join([title, price_full, description, complete_href])
            last_posts.append(Post(id=id_post, href=complete_href, description=description, image=image_src,
                                   price=price))
        return last_posts


def cleaning_spaces(txt):
    return ' '.join(txt.split())
