# coding=utf-8

import re

import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import load_only

from db import session, Post

id_regex = re.compile('(\d+).htm')


class MilanunciosCrawler:
    def __init__(self, url):
        self.url = url
        self.last_posts = []
        self.new_posts = []

    def get_last_posts(self):
        self.last_posts = []
        r = requests.get(self.url)
        html = BeautifulSoup(r.content, 'html.parser')
        raw_posts = html.findAll("div", {"class": "aditem-detail-image-container"})

        for post in raw_posts:
            title_element = post.find("a", {"class": "aditem-detail-title"})
            title = title_element.text
            description = post.find("div", {"class": "tx"}).text
            href = title_element['href']
            id_post = id_regex.search(href).group(1)
            type_rent = post.find("div", {"class": "pillDiv"}).text
            price = post.find("div", {"class": "aditem-price"}).text
            image_element = post.find("img", {"class": "ee"})
            image = image_element['src'] if image_element else ''
            other_info = ' '.join([tag.text for tag in post.findAll("div", {"class": "tag-mobile"})])

            description = '\n'.join([title, description, type_rent, other_info, price])

            self.last_posts.append(dict(id=int(id_post),
                                        href=href,
                                        description=description,
                                        image=image))

    def get_new_posts(self):
        existings = [found.id for found in session.query(Post).filter(
            Post.id.in_([post['id'] for post in self.last_posts])).options(load_only("id")).all()]
        self.new_posts = list(filter(lambda x: x['id'] not in existings, self.last_posts))

    def store_new_posts(self):
        session.add_all([Post(**new_post) for new_post in self.new_posts])
        session.commit()

    def get(self):
        self.get_last_posts()
        self.get_new_posts()
        self.store_new_posts()
        return [{'text': '{}\n{}'.format(post['description'], 'https://www.milanuncios.com{}'.format(post['href'])),
                 'image': post['image']} for post in self.new_posts]
