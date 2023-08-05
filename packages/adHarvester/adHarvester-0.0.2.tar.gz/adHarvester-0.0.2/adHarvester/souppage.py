import json
from json import JSONDecodeError

import js2py
from bs4 import BeautifulSoup
import logging
from js2py.base import JsObjectWrapper
from js2py.internals.simplex import JsException


def does_nested_key_exists(element, key):
    if key in element.keys():
        return element[key]

    for k, v in element.items():
        if isinstance(v, dict):
            item = does_nested_key_exists(v, key)
            if item is not None:
                return item
        if isinstance(v, list):
            item = None
            for i in v:
                if isinstance(i, dict):
                    item = does_nested_key_exists(i, key)
            if item is not None:
                return item


class BaseSelector:
    _name: str = None
    _required_attr: str = None

    def __init__(self, name: str, required_attr=None):
        self._name = name
        self._required_attr = required_attr

    def __str__(self) -> str:
        return 'name is {}, required attr is {}'.format(self._name, self._required_attr)

    @property
    def get_name(self) -> str:
        return self._name

    @property
    def get_required_attr(self):
        return self._required_attr


class Selector(BaseSelector):
    _selector_type: str = True
    _attr: dict = None

    def __init__(self, name: str, selector_type='css', attr=None, required_attr=None):
        super().__init__(name, required_attr)
        self._selector_type = selector_type
        self._attr = attr

    @property
    def get_selector_type(self) -> str:
        return self._selector_type

    @property
    def get_attr(self):
        return self._attr


class SoupPage:
    _soup = None
    _html = None

    def __init__(self, html):
        self._html = html
        self._soup = BeautifulSoup(html, 'lxml')

    def find(self, needle):
        """Function to find identifier of given needle"""
        logging.debug("Running SoupPage:find method")
        print(self)
        assert type(needle) == str, "can only find strings, %s given" % type(needle)

    def select(self, selector: Selector):
        logging.debug("Running SoupPage:select method")
        logging.info("Selector type is {}".format(selector.get_selector_type))
        if selector.get_selector_type == 'meta':
            return [res.get(selector.get_required_attr) if selector.get_required_attr else res.text for res in
                    self._soup.find_all('meta', {'name': selector.get_name})]
        elif selector.get_selector_type == 'css':
            return [res.get(selector.get_required_attr) if selector.get_required_attr else res.text for res in
                    self._soup.select(selector.get_name)]
        elif selector.get_selector_type == 'tag':
            # Select info based on Selector inputs
            if selector.get_attr is None:
                data = self._soup.find_all(selector.get_name)
            elif selector.get_name != '':
                data = self._soup.find_all(selector.get_name, selector.get_attr)
            else:
                data = self._soup.find_all(attrs=selector.get_attr)
            return [res.get(selector.get_required_attr) if selector.get_required_attr else res.text for res in data]
        elif selector.get_selector_type == 'script':
            data = []
            if selector.get_attr.get('tag_attr') is None:
                data = self._soup.find_all(selector.get_name)
            elif selector.get_name != '':
                data = self._soup.find_all(selector.get_name, selector.get_attr.get('tag_attr'))
            temp = []
            for index, res in enumerate(data):
                try:
                    json_data = js2py.eval_js(res.text)
                    if json_data is not None and type(json_data) == JsObjectWrapper:
                        temp.append(json_data.to_dict())
                except JsException:
                    try:
                        json_data = json.loads(res.text, strict=False)
                        temp.append(json_data)
                    except JSONDecodeError:
                        pass
            #pprint(temp)
            return_data = []
            for d in temp:
                for key in selector.get_attr.get('keywords'):
                    temp_data = does_nested_key_exists(d, key)
                    if temp_data is not None:
                        return_data.append(temp_data)
            return return_data
        elif selector.get_selector_type == 'table':
            logging.info("Selector type is table")
            table = self._soup.select(selector.get_name)
            if len(table) > 0:
                table = table[0]
            else:
                return []
            headers = table.find_all(
                selector.get_attr.get('master').get('tag'),
                selector.get_attr.get('master').get('attr')
            )
            data = []
            for head in headers:
                if selector.get_attr.get('keyword') in str(head):
                    if selector.get_attr.get('slave') == selector.get_attr.get('master'):
                        temp = head
                    else:
                        temp = head.find(
                            selector.get_attr.get('slave').get('tag'),
                            selector.get_attr.get('slave').get('attr')
                        )
                    if temp is not None:
                        data.append(temp)
            return [res.get(selector.get_required_attr) if selector.get_required_attr else res.text for res in data]
        else:
            print("Selector type is not provided!")
            logging.warning("Selector type is not provided!")
            return []
