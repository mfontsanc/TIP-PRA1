import requests
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self, url):
        self.url = url
        self.output_data = []
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,\
            */*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "en-US,en;q=0.8",
            "Cache-Control": "no-cache",
            "dnt": "1",
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
            (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"
        }

    def __download_web(self):
        """
        Descarrega la web guardada a la variable self.url
        :return: Objecte del tipus BeautifulSoup (contingut de la web en HTML)
        """
        page = requests.get(self.url, self.headers)

        if page.status_code == 200:
            return BeautifulSoup(page.content, "html.parser")

    def __get_links(self, content):
        """
        Obté els links de l'objecte tipus BeautifulSoup
        :return: null
        """
        list_categories = self.__get_categories(content)
        print(list_categories)

    def __get_categories(self, content):
        """
        Obté el llistat de categories (nom) i la URL d'accés.
        :param content: Objecte del tipus BeautifulSoup
        :return: list_categories: Array
        """
        categories = content.find("div", {"data-component": "navigation-bar"})
        categories_a = categories.findChildren("a", recursive=True)
        list_categories = []

        for category_a in categories_a:
            href = self.url + category_a.get('href')
            name = category_a.get('title')

            if href and name:
                list_categories.append([name, href])

        return list_categories

    def init_process(self):
        """
        Executa el procés de web scraping
        :return: null
        """
        content_html = self.__download_web()
        self.__get_links(content_html)
