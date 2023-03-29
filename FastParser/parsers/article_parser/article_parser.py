from typing import Generator
import bs4.element
import cfscrape
from urllib3.util import parse_url
from bs4 import BeautifulSoup


class ParseUrl:

    def __init__(self, url: str):
        """
        Web scrapper initialization
        """
        self.url = url
        self.parsed_url = parse_url(self.url)
        self.url_schema = self.parsed_url.scheme
        self.domain = self.url_schema + "://" + self.parsed_url.host
        scrapper = cfscrape.create_scraper()
        markup = scrapper.get(url=self.url).text
        self.bs_parser = BeautifulSoup(markup, "lxml")

    def get_header(self) -> str:
        """
        Get title of an article
        """
        header = self.bs_parser.find("h1").text
        return header

    def get_article_text(self) -> str:
        """
        Get text of an article
        """
        article = self.bs_parser.find_all("p")
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

    def get_article_images(self, count: int = 5) -> list[str]:
        """
        Get images from article
        """
        images = self.bs_parser.find_all("img")
        images = list(self.check_image(images))[:count]
        return images
