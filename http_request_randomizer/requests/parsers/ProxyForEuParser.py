import logging

import requests
from bs4 import BeautifulSoup

from http_request_randomizer.requests.parsers.UrlParser import UrlParser
from http_request_randomizer.requests.proxy.ProxyObject import ProxyObject, AnonymityLevel

logger = logging.getLogger(__name__)
__author__ = 'pgaref'


class ProxyForEuParser(UrlParser):
    def __init__(self, id, web_url, bandwidth=None, timeout=None):
        UrlParser.__init__(self, id=id, web_url=web_url, bandwidth_KBs=bandwidth, timeout=timeout)

    def parse_proxyList(self):
        curr_proxy_list = []
        try:
            response = requests.get(self.get_url(), timeout=self.timeout)

            if not response.ok:
                logger.warning("Proxy Provider url failed: {}".format(self.get_url()))
                return []

            content = response.content
            soup = BeautifulSoup(content, "html.parser")
            table = soup.find("table", attrs={"class": "proxy_list"})

            # The first tr contains the field names.
            headings = [th.get_text() for th in table.find("tr").find_all("th")]

            datasets = []
            for row in table.find_all("tr")[1:]:
                dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
                datasets.append(dataset)

            for dataset in datasets:
                # Avoid Straggler proxies and make sure it is a Valid Proxy Address
                proxy_obj = self.create_proxy_object(dataset)
                if proxy_obj is not None and UrlParser.valid_ip_port(proxy_obj.get_address()):
                    curr_proxy_list.append(proxy_obj)
                else:
                    logger.debug("Proxy Invalid: {}".format(dataset))
        except AttributeError as e:
            logger.error("Provider {0} failed with Attribute error: {1}".format(self.id, e))
        except KeyError as e:
            logger.error("Provider {0} failed with Key error: {1}".format(self.id, e))
        except Exception as e:
            logger.error("Provider {0} failed with Unknown error: {1}".format(self.id, e))
        finally:
            return curr_proxy_list

    def create_proxy_object(self, dataset):
        ip = ""
        port = None
        anonymity = AnonymityLevel.UNKNOWN
        country = None
        # Check Field[0] for tags and field[1] for values!
        for field in dataset:
            # Discard slow proxies! Speed is in KB/s
            if field[0] == 'Speed':
                if float(field[1]) < self.get_min_bandwidth():
                    logger.debug("Proxy with low bandwidth: {}".format(float(field[1])))
                    return None
            if field[0] == 'IP':
                ip = field[1].strip()  # String strip()
                # Make sure it is a Valid IP
                if not UrlParser.valid_ip(ip):
                    logger.debug("IP with Invalid format: {}".format(ip))
                    return None
            elif field[0] == 'Port':
                port = field[1].strip()  # String strip()
            elif field[0] == 'Anon':
                anonymity = AnonymityLevel.get(field[1].strip())  # String strip()
            elif field[0] == 'Country':
                country = field[1].strip()  # String strip()
        return ProxyObject(source=self.id, ip=ip, port=port, anonymity_level=anonymity, country=country)

    def __str__(self):
        return "ProxyForEU Parser of '{0}' with required bandwidth: '{1}' KBs" \
            .format(self.url, self.minimum_bandwidth_in_KBs)
