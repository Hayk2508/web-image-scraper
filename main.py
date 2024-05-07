from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urlparse, urljoin
import argparse
import validators


class Parser(ABC):
    @abstractmethod
    def parse(self, url: str):
        pass


class ImgParser(Parser):
    def __init__(self):
        self.image_urls = []

    def parse(self, url: str):
        html_content = requests.get(url).text
        soup = BeautifulSoup(html_content, 'lxml')
        img_tags = soup.find_all('img')
        for img in img_tags:
            img_url = img.get('src')
            if not img_url.startswith(('http://', 'https://')):
                base_url = '{uri.scheme}://{uri.netloc}'.format(uri=urlparse(url))
                img_url = urljoin(base_url, img_url)
            self.image_urls.append(img_url)

    def download_image(self, img_url: str, directory: str):
        img_name = os.path.basename(img_url)
        abs_path = os.path.join(directory, img_name)
        with open(abs_path, 'wb') as file:
            file.write(requests.get(img_url).content)

    def save_images(self, directory: str):
        for img_url in self.image_urls:
            self.download_image(img_url=img_url, directory=directory)


def main():
    parser = argparse.ArgumentParser(description='Download images from a webpage.')
    parser.add_argument('-url', '--url', type=str, help='URL of the webpage containing images')
    parser.add_argument('-d', '--directory', type=str, help='Directory to save downloaded images')
    args = parser.parse_args()

    url = args.url
    directory = args.directory

    if url is None or directory is None:
        print("Error: Please provide both URL and directory arguments.")
        return

    if not validators.url(url):
        print("Error: Invalid URL provided.")
        return

    if not os.path.exists(directory):
        os.makedirs(directory)

    img_parser = ImgParser()
    img_parser.parse(url=url)
    img_parser.save_images(directory=directory)
    print("Images downloaded successfully.")


if __name__ == "__main__":
    main()
