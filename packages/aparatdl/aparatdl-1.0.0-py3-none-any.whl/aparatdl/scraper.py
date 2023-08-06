import requests
from bs4 import BeautifulSoup
from aparatdl.exceptions import QualityError


class Scraper:
    def __init__(self,url,quality=None):
        self.url = url
        self.quality = quality

    def get_data(self):
        get_data = requests.get(self.url)
        content = BeautifulSoup(get_data.text, 'html.parser')
        get_tag_links = content.findAll('li', {'class': 'menu-item-link link'})
        return get_tag_links

    def get_all_links(self):
        get_tag_links = self.get_data()
        links = [li.a['href'] for li in get_tag_links]
        return links

    def get_all_quality(self):
        get_tag_links = self.get_data()
        aria_label = [[i for i in li.a['aria-label'].split()] for li in get_tag_links]
        qualities = [i[-1] for i in aria_label]
        return qualities

    def get_link(self):
        qualities = self.get_all_quality()
        links = self.get_all_links()
        if self.quality not in qualities:
            raise QualityError(f'this is a quality ({self.quality}) is not available!!!\n'
                               f'the available qualities are {qualities}')
        else:
            index = None
            for i in range(len(qualities)):
                if qualities[i] == self.quality:
                    index = i
        return links[index]
