import logging

import requests
from bs4 import BeautifulSoup

from http_request_randomizer.requests.parsers.UrlParser import UrlParser
from http_request_randomizer.requests.proxy.ProxyObject import ProxyObject

logger = logging.getLogger(__name__)
__author__ = 'pgaref'


class FreeProxyParser(UrlParser):
    def __init__(self, web_url, timeout=None):
        UrlParser.__init__(self, web_url, timeout)

    def parse_proxyList(self):
        curr_proxy_list = []
        response = requests.get(self.get_URl(), timeout=self.timeout)

        if not response.ok:
            logger.warn("Proxy Provider url failed: {}".format(self.get_URl()))
            return []

        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        table = soup.find("table", attrs={"id": "proxylisttable"})

        # The first tr contains the field names.
        headings = [th.get_text() for th in table.find("tr").find_all("th")]

        datasets = []
        for row in table.find_all("tr")[1:]:
            dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
            if dataset:
                datasets.append(dataset)

        for dataset in datasets:
            # Check Field[0] for tags and field[1] for values!
            address = ""
            for field in dataset:
                if field[0] == 'IP Address':
                    # Make sure it is a Valid IP
                    if not UrlParser.valid_ip(field[1]):
                        logger.debug("IP with Invalid format: {}".format(field[1]))
                        break
                    else:
                        address += field[1] + ':'
                        proxy_object = ProxyObject()
                        proxy_object.ip_address = field[1]
                elif field[0] == 'Port':
                    address += field[1]
                    proxy_object.port = field[1]
                elif field[0] == 'Anonymity':
                    proxy_object.anonymity_level = field[1]
                elif field[0] == 'Country':
                    proxy_object.country = field[1]
            # Make sure it is a Valid Proxy Address
            if UrlParser.valid_ip_port(address):
                proxy = "http://" + address
                curr_proxy_list.append(proxy.__str__())
                proxy_object.print_everything()
            else:
                logger.debug("Address with Invalid format: {}".format(address))
            # print "{0:<10}: {1}".format(field[0], field[1])
        # print "ALL: ", curr_proxy_list
        return curr_proxy_list

    def __str__(self):
        return "FreeProxy Parser of '{0}' with required bandwidth: '{1}' KBs" \
            .format(self.url, self.minimum_bandwidth_in_KBs)
