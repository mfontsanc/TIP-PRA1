import requests
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self, url):
        self.url = url
        self.output_data = []

    def __download_web(self):
        """
        Descarrega la web guardada a la variable self.url
        :return: Objecte del tipus BeautifulSoup (contingut de la web en HTML)
        """
        page = requests.get(self.url)

        if page.status_code == 200:
            return BeautifulSoup(page.content, "html.parser")

    def __get_links(self, content):
        """
        Obté els links de l'objecte tipus BeautifulSoup
        :return: null
        """
        list_categories = self.__get_categories(content)

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
