import requests
import json
import csv
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self, url):
        self.url = url
        self.output_data = []
        self.output_file = "../csv/ArticlesTimeOutCat.csv"
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

    def download_web(self, url):
        """
        Descarrega la web guardada a la variable self.url
        :return: Objecte del tipus BeautifulSoup (contingut de la web en HTML)
        """
        try:
            page = requests.get(url)

            if page.status_code == 200:
                return BeautifulSoup(page.content, "html.parser")
        except:
            print("Error getting the URL, the process continues: " + url)

    def get_links(self, content):
        """
        Obté els links de l'objecte tipus BeautifulSoup
        :return: null
        """
        list_categories = self.get_categories(content)

        return list_categories

    def get_categories(self, content):
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

            if href and name and name != 'Separator':
                list_categories.append([name, href])

        return list_categories

    def get_articles(self, content):
        """
        Donat la URL d'una categoria,
        obté el llistat d`'URL d'accés dels articles
        :param content: Objecte del tipus String
        :return: list_: Array
        """
        content_html = self.download_web(content)

        if content_html:
            articles = content_html.findChildren("article", recursive=True)
            list_articles = []

            for articles_a in articles:
                href_ = articles_a.find('a')
                if href_:
                    url_art = href_.get('href')
                    if url_art and url_art != '[cta_link]' and (url_art.startswith('https://www.timeout.cat/')
                                                                or not url_art.startswith('http')):
                        list_articles.append(url_art)

            return list_articles

    def get_details(self, url, category):
        """
        Donat la URL d'un article, obté la informació de l'article que volem
        guardar en el csv.
        :param category: category on s'ha trobat l'article i la URL.
        :param url: URL amb els detalls de l'article.
        :return: None
        """
        content_html = self.download_web(url)

        if content_html:
            data_str = content_html.find("script", {"type": "application/ld+json"})

            if data_str:
                data_json = json.loads(data_str.contents[0])
                if data_json['@type'] == 'Article':
                    self.output_data.append({
                        "categoria": category[0],
                        "urlCategoria": category[1],
                        "article": data_json['name'],
                        "descripcio": data_json['description'],
                        "tipus": data_json['@type'],
                        "urlArticle": url,
                        "creador": data_json['creator'],
                        "dataPublicacio": data_json['datePublished'],
                        "paraulesClaus": data_json['keywords']
                    })

    def save_csv(self):
        """
        Guarda les dades obtingudes en un CSV.
        :return: None
        """
        header = ['categoria', 'urlCategoria', 'article', 'descripcio', 'tipus', 'urlArticle', 'creador',
                  'dataPublicacio', 'paraulesClaus']

        file = open(self.output_file, 'w', newline='', encoding="utf-8-sig")
        writer = csv.writer(file, delimiter=";")
        # Guarda els headers
        writer.writerow(header)
        # Guarda la informació de la variable output_data
        for data in self.output_data:
            writer.writerow(list(data.values()))

        file.close()

    def init_csv(self, content):
        for content_a in content:
            print("Getting articles with the category: " + content_a[0])
            articles = self.get_articles(content_a[1])
            for articles_a in articles:
                if "//www.timeout.cat/" not in articles_a:
                    articles_a = self.url + articles_a
                self.get_details(articles_a, content_a)

        print("Saving data into the dataset.")
        self.save_csv()

    def init_process(self):
        """
        Executa el procés de web scraping
        :return: null
        """
        print("Starting process...")
        content_html = self.download_web(self.url)

        if content_html:
            links_url = self.get_links(content_html)
            print("Total number of categories: ", len(links_url))
            self.init_csv(links_url)
            print("Dataset has been created: " + self.output_file)
        else:
            print("Web scraping process ended without results!")
