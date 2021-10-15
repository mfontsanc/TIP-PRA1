import requests
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self, url):
        self.url = url
        self.output_data = []

    def __download_web(self):
        page = requests.get(self.url)

        if page.status_code == 200:
            return BeautifulSoup(page.content)

    def init_process(self):
        content_html = self.__download_web()
        print(content_html.prettify())
