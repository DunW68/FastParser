from typing import Generator
import bs4.element
import cfscrape
from urllib3.util import parse_url
from bs4 import BeautifulSoup


class ParseUrl:

    def __init__(self, url: str):
        self.url = url
        self.parsed_url = parse_url(self.url)
        self.url_schema = self.parsed_url.scheme
        self.domain = self.url_schema + "://" + self.parsed_url.host

    def init_scrapper(self) -> BeautifulSoup:
        """
        Web scrapper initialization
        """
        scrapper = cfscrape.create_scraper()
        markup = scrapper.get(url=self.url).text
        bs_parse = BeautifulSoup(markup, "lxml")
        return bs_parse

    def get_header(self, bs_parse: BeautifulSoup) -> str:
        """
        Get title of an article
        """
        header = bs_parse.find("h1").text
        return header

    def get_article(self, bs_parse: BeautifulSoup) -> str:
        """
        Get text of an article
        """
        article = bs_parse.find_all("p")
        article = " ".join(self.delete_article_garbage(article_list=article))
        return article

    def delete_article_garbage(self, article_list: bs4.element.ResultSet) -> list[str]:
        """
        Delete tags, attributes, etc. from article
        """
        new_result = [line.text for line in article_list]
        return new_result

    def check_image(self, images: bs4.element.ResultSet) -> Generator:
        """
        Check images that have jpeg or jpg extension
        """
        for image in images:
            image = image["src"]
            if image.endswith("jpg") or image.endswith("jpeg"):
                if image.startswith("//"):
                    image = image[2:]
                elif image.startswith("/"):
                    image = self.url_schema + "://" + image
                yield image

    def get_article_images(self, bs_parse: BeautifulSoup, count: int = 5):
        """
        Get images from article
        """
        images = bs_parse.find_all("img")
        images = list(self.check_image(images))[:count]
        return images

    def parse_url(self):
        """
        Main parser function
        """
        bs_parse = self.init_scrapper()
        header = self.get_header(bs_parse=bs_parse)
        article = self.get_article(bs_parse=bs_parse)
        images = self.get_article_images(bs_parse=bs_parse, count=3)
