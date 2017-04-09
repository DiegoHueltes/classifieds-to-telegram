# coding=utf-8


import requests
from bs4 import BeautifulSoup

from crawlers.crawler_base import Crawler
from db.models import Post


class WallapopCrawler(Crawler):
    """
    Crawler specific to gather the information from the web https://es.wallapop.com
    """
    crawler_url = 'https://es.wallapop.com'
    web_type = 'WALLAPOP'

    def __init__(self, target_url, *args, **kwargs):
        super(WallapopCrawler, self).__init__(*args, **kwargs)
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
        raw_posts = html.findAll("div", {"class": "card-product"})

        for post in raw_posts:
            title_element = post.find("a", {"class": "product-info-title"})
            if not title_element:
                continue
            title = cleaning_spaces(self.text(title_element))
            href = title_element['href']
            description = self.text(post.find("a", {"class": "product-info-category"}))
            id_post = str(href.split('-')[-1])
            price_full = cleaning_spaces(self.text(post.find("span", {"class": "product-info-price"})))
            price = int(price_full[:-1].replace('.', ''))  # Removing currency symbol
            image_element = post.find('img', {'class': 'card-product-image'})
            image_src = None
            if image_element:
                image_src = image_element.get('src', '')
            complete_href = self.crawler_url + href
            description = '\n'.join([title, price_full, cleaning_spaces(description), complete_href])
            last_posts.append(Post(id=id_post, href=complete_href, description=description, image=image_src,
                                   price=price))
        return last_posts


def cleaning_spaces(txt):
    try:
        if not txt:
            return ''
        return ' '.join(txt.split())
    except:
        print(txt)
