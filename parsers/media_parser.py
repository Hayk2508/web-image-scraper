import os
from abc import ABC
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
from .parser_abc import Parser


class MediaParser(Parser, ABC):

    def __init__(self, url, directory):
        super().__init__(url=url)
        self.directory = directory

    def download(self, url):
        video_name = os.path.basename(url)
        abs_path = os.path.join(self.directory, video_name)
        with open(abs_path, 'wb') as file:
            file.write(requests.get(media_url).content)

    def process_url(self, url):
        base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(self.url))
        url = urljoin(base_url, url)
        return url

    def fetch(self, tag: str):
        html_content = requests.get(self.url).content
        soup = BeautifulSoup(html_content, 'lxml')
        tags = soup.find_all(tag)
        return tags