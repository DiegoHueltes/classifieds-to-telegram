# coding=utf-8


import requests
from bs4 import BeautifulSoup

from crawlers.crawler_base import Crawler
from db.models import Post


class IdealistaCrawler(Crawler):
    """
    Crawler specific to gather the information from the web www.idealista.com
    """
    crawler_url = 'https://www.idealista.com'
    web_type = 'IDEALISTA'

    def __init__(self, target_url, *args, **kwargs):
        super(IdealistaCrawler, self).__init__(*args, **kwargs)
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
        raw_posts = html.findAll("div", {"class": "item"})

        for post in raw_posts:
            title_element = post.find("a", {"class": "item-link"})
            title = title_element.text
            href = title_element['href']
            description = post.find("div", {"class": "item-info-container"}).text
            id_post = int(post['data-adid'])
            price = post.find("span", {"class": "item-price"}).text
            image_element = post.find_all("img")
            image_src = image_element[0]['data-ondemand-img'] if image_element else None
            complete_href = self.crawler_url + href
            description = '\n'.join([title, description, price, complete_href])
            last_posts.append(Post(id=id_post, href=complete_href, description=description, image=image_src))
        return last_posts
