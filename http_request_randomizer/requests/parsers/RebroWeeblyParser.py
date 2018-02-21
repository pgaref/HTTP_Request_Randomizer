import logging

import requests
from bs4 import BeautifulSoup

from http_request_randomizer.requests.parsers.UrlParser import UrlParser
from http_request_randomizer.requests.proxy.ProxyObject import ProxyObject, AnonymityLevel

logger = logging.getLogger(__name__)
__author__ = 'pgaref'


class RebroWeeblyParser(UrlParser):
    def __init__(self, id, web_url, timeout=None):
        self.top_proxy_path = "proxy-list.html"
        self.txt_proxy_path = "txt-lists.html"
        UrlParser.__init__(self, id=id, web_url=web_url, timeout=timeout)

    def parse_proxyList(self, use_top15k=False):
        curr_proxy_list = []
        try:
            response = requests.get(self.get_url() + "/" + self.top_proxy_path, timeout=self.timeout)

            if not response.ok:
                logger.warning("Proxy Provider url failed: {}".format(self.get_url()))
                return []

            content = response.content
            soup = BeautifulSoup(content, "html.parser")
            all_divs = soup.findAll("div", attrs={"class": "paragraph", 'style': "text-align:left;"})
            # address_table = soup.find("div", attrs={"class": "paragraph", 'style': "text-align:left;"})
            # .find('font', attrs={'color': '#33a27f'})
            # Parse Top Proxy List page
            address_list = []
            country_list = []
            anonymity_list = []
            for div in all_divs:
                address_div = div.find('font', attrs={'color': '#33a27f'})
                if address_div is not None:
                    for row in [x for x in address_div.contents if getattr(x, 'name', None) != 'br']:
                        address_list.append(str(row))
                curr_div = div.findAll('font', attrs={'size': '2'})
                if curr_div[0] is not None:
                    row_data = []
                    # font -> strong -> font
                    title = curr_div[0].contents[0].contents[0].contents[0]
                    for row in [x for x in curr_div[-1].contents if getattr(x, 'name', None) != 'br']:
                        row_data.append(str(row))
                    if 'Country' in str(title):
                        country_list.extend(row_data)
                    if 'Status' in str(title):
                        anonymity_list.extend(row_data)
            for address, country, anonymity in zip(address_list, country_list, anonymity_list):
                # Make sure it is a Valid Proxy Address
                proxy_obj = self.create_proxy_object(address, country, anonymity)
                if proxy_obj is not None and UrlParser.valid_ip_port(proxy_obj.get_address()):
                    curr_proxy_list.append(proxy_obj)
                else:
                    logger.debug("Proxy Invalid: {}".format(row))
            # Usually these proxies are stale
            if use_top15k:
                # Parse 15k Nodes Text file (named *-all-*.txt)
                content = requests.get(self.get_url() + "/" + self.txt_proxy_path).content
                soup = BeautifulSoup(content, "html.parser")
                table = soup.find("div", attrs={"class": "wsite-multicol-table-wrap"})
                for link in table.findAll('a'):
                    current_link = link.get('href')
                    if current_link is not None and "all" in current_link:
                        self.txt_proxy_path = current_link
                more_content = requests.get(self.get_url() + self.txt_proxy_path).text
                for proxy_address in more_content.split():
                    if UrlParser.valid_ip_port(proxy_address):
                        proxy_obj = self.create_proxy_object(row)
                        curr_proxy_list.append(proxy_obj)
        except AttributeError as e:
            logger.error("Provider {0} failed with Attribute error: {1}".format(self.id, e))
        except KeyError as e:
            logger.error("Provider {0} failed with Key error: {1}".format(self.id, e))
        except Exception as e:
            logger.error("Provider {0} failed with Unknown error: {1}".format(self.id, e))
        finally:
            return curr_proxy_list

    def create_proxy_object(self, address, country, anonymity):
        # Make sure it is a Valid IP
        ip = address.strip().split(":")[0]
        if not UrlParser.valid_ip(ip):
            logger.debug("IP with Invalid format: {}".format(ip))
            return None
        port = address.strip().split(":")[1]
        country = country.strip()
        anonymity = AnonymityLevel.get(anonymity.strip())

        return ProxyObject(source=self.id, ip=ip, port=port, anonymity_level=anonymity, country=country)

    def __str__(self):
        return "RebroWeebly Parser of '{0}' with required bandwidth: '{1}' KBs" \
            .format(self.url, self.minimum_bandwidth_in_KBs)
