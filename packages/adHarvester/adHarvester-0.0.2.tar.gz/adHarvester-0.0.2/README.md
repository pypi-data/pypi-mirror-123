# Ad Harvester
## _Very useful package to scrap data from website_

[![N|Solid](https://cldup.com/dTxpPi9lDf.thumb.png)](https://nodesource.com/products/nsolid)

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)

AdHarvester is a libarary which aloow you to scrap website information by just modifiying input json.

- Create json file or python dict with input information
- Import package Classes
- ✨Magic ✨

## Tech

adHarvester uses a number of open source projects to work properly:

- [bs4] - Beautiful Soup is a Python library for pulling data out of HTML and XML files
- [js2py] - Translates JavaScript to Python code
- [requests] - Requests is an elegant and simple HTTP library for Python, built for human beings.

And of course adHarvester itself is open source with a [public repository][dill]
 on GitHub.

## Installation

AdHarvester requires [Python](https://python.org/) v3+ to run.

Install the dependencies.

```sh
cd adHarvester
pip install -r requirements.txt
```
## Examples

Input Example

```python
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
```

How to use library?

```python
import requests
from adHarvester import Harvester

test_url = "https://www.adverts.ie/car/opel/insignia/2010-opel-insignia/25079005"
r = requests.get(test_url)
my_html = r.text


h = Harvester(donedeal_new_car_rules)
h.init_rules()

print(h.scrap_from_html(my_html))

```

Another Example

```python
import requests
from adHarvester import Harvester

test_url = "https://www.donedeal.ie/new-car-for-sale/nissan/leaf/hatchback?campaign=21"

h = Harvester(donedeal_new_car_rules)
h.init_rules()

print(h.scrap_from_html(test_url))
```

## License

MIT

**Free Software, Hell Yeah!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/surenab/adHarvester>
   [git-repo-url]: <https://github.com/surenab/adHarvester.git>
   [bs4]: <https://www.crummy.com/software/BeautifulSoup/bs4/doc/>
   [js2py]: <https://pypi.org/project/Js2Py/>
   [requests]: <https://docs.python-requests.org/en/latest/>
    