import requests
from souppage import SoupPage, Selector


class Harvester:
    _selectors: dict = {}
    _rules: dict = {}

    def __init__(self, rules: dict = None):
        self._rules = rules

    def init_rules(self):
        for key in self._rules.keys():
            self._selectors[key] = Selector(self._rules[key].get('name'),
                                            self._rules[key].get('selector_type'),
                                            attr=self._rules[key].get('attr'),
                                            required_attr=self._rules[key].get('required_attr'))

    @property
    def get_selectors(self):
        return self._selectors

    @property
    def get_rules(self):
        return self._rules

    def set_rules(self, rules):
        self._rules = rules

    def scrap_from_html(self, html):
        soup_page = SoupPage(html)
        data = {}
        for key in self._selectors.keys():
            data[key] = soup_page.select(self._selectors.get(key))
        return data

    def scrap_from_url(self, url):
        response = requests.get(url)
        return self.scrap_from_html(response.text)




test_url = "https://www.adverts.ie/car/opel/insignia/2010-opel-insignia/25079005"

r = requests.get(test_url)
my_html = r.text

f = open('carzone.html', 'w')
f.write(my_html)
f.close()


donedeal_new_car_rules = {
    'price': {'name': 'div.c-overview-panel__info.key-info > ul',
              'selector_type': 'table',
              'attr': {'master': {'tag': 'li', },
                       'slave': {'tag': 'span', 'attr': {'class': 'attr-value'}},
                       'keyword': 'Price', }
              },
    'fuel_type': {'name': 'div.c-overview-panel__info.key-info > ul',
                  'selector_type': 'table',
                  'attr': {'master': {'tag': 'li', },
                           'slave': {'tag': 'span', 'attr': {'class': 'attr-value'}},
                           'keyword': 'Fuel Type', }
                  },
    'make': {'name': 'span > a:nth-child(3) > span',
             'selector_type': 'css'},
    'model': {'name': 'span > a:nth-child(4) > span',
              'selector_type': 'css'},
    'header': {'name': '#js-react-page > div > div:nth-child(3) > div > div > div:nth-child(2) > h1',
               'selector_type': 'css'},
}

h = Harvester(donedeal_new_car_rules)
h.init_rules()

print(h.scrap_from_html(my_html))
