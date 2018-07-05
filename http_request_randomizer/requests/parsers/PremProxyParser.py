import logging

import requests
from bs4 import BeautifulSoup

from http_request_randomizer.requests.parsers.js.UnPacker import JsUnPacker
from http_request_randomizer.requests.parsers.UrlParser import UrlParser
from http_request_randomizer.requests.proxy.ProxyObject import ProxyObject, AnonymityLevel, Protocol

logger = logging.getLogger(__name__)
__author__ = 'pgaref'


# Samair Proxy now renamed to: premproxy.com
class PremProxyParser(UrlParser):
    def __init__(self, id, web_url, timeout=None):
        self.base_url = web_url
        web_url += "/list/"
        # Ports decoded by the JS unpacker
        self.js_unpacker = None
        UrlParser.__init__(self, id=id, web_url=web_url, timeout=timeout)

    def parse_proxyList(self):
        curr_proxy_list = []
        try:
            # Parse all proxy pages -> format: /list/{num}.htm
            # Get the pageRange from the 'pagination' table
            page_set = self.get_pagination_set()
            logger.debug("Pages: {}".format(page_set))
            # One JS unpacker per provider (not per page)
            self.js_unpacker = self.init_js_unpacker()

            for page in page_set:
                response = requests.get("{0}{1}".format(self.get_url(), page), timeout=self.timeout)
                if not response.ok:
                    # Could not parse ANY page - Let user know
                    if not curr_proxy_list:
                        logger.warning("Proxy Provider url failed: {}".format(self.get_url()))
                    # Return proxies parsed so far
                    return curr_proxy_list
                content = response.content
                soup = BeautifulSoup(content, "html.parser", from_encoding="iso-8859-1")

                table = soup.find("div", attrs={"id": "proxylist"})
                # The first tr contains the field names.
                headings = [th.get_text() for th in table.find("tr").find_all("th")]
                # skip last 'Select All' row
                for row in table.find_all("tr")[1:-1]:
                    td_row = row.find("td")
                    portKey = td_row.find('span', attrs={'class': True}).get('class')[0]
                    port = self.js_unpacker.get_port(portKey)
                    proxy_obj = self.create_proxy_object(row, port)
                    # Make sure it is a Valid Proxy Address
                    if proxy_obj is not None and UrlParser.valid_ip(proxy_obj.ip) and UrlParser.valid_port(port):
                        curr_proxy_list.append(proxy_obj)
                    else:
                        logger.debug("Proxy Invalid: {}".format(proxy_obj.to_str()))
        except AttributeError as e:
            logger.error("Provider {0} failed with Attribute error: {1}".format(self.id, e))
        except KeyError as e:
            logger.error("Provider {0} failed with Key error: {1}".format(self.id, e))
        except Exception as e:
            logger.error("Provider {0} failed with Unknown error: {1}".format(self.id, e))
        finally:
            return curr_proxy_list

    def get_pagination_set(self):
        response = requests.get(self.get_url(), timeout=self.timeout)
        page_set = set()
        # Could not parse pagination page - Let user know
        if not response.ok:
            logger.warning("Proxy Provider url failed: {}".format(self.get_url()))
            return page_set
        content = response.content
        soup = BeautifulSoup(content, "html.parser")
        for ultag in soup.find_all('ul', {'class': 'pagination'}):
            for litag in ultag.find_all('li'):
                page_ref = litag.a.get('href')
                # Skip current page '/list'
                if page_ref.endswith(('htm', 'html')):
                    page_set.add(page_ref)
                else:
                    page_set.add("")
        return page_set

    def init_js_unpacker(self):
        response = requests.get(self.get_url(), timeout=self.timeout)
        # Could not parse provider page - Let user know
        if not response.ok:
            logger.warning("Proxy Provider url failed: {}".format(self.get_url()))
            return None
        content = response.content
        soup = BeautifulSoup(content, "html.parser")

        # js file contains the values for the ports
        for script in soup.findAll('script'):
            if '/js/' in script.get('src'):
                jsUrl = self.base_url + script.get('src')
                return JsUnPacker(jsUrl)
        return None

    def create_proxy_object(self, row, port):
        for td_row in row.findAll("td"):
            if td_row.attrs['data-label'] == 'IP:port ':
                text = td_row.text.strip()
                ip = text.split(":")[0]
                # Make sure it is a Valid IP
                if not UrlParser.valid_ip(ip):
                    logger.debug("IP with Invalid format: {}".format(ip))
                    return None
            elif td_row.attrs['data-label'] == 'Anonymity Type: ':
                anonymity = AnonymityLevel.get(td_row.text.strip())
            elif td_row.attrs['data-label'] == 'Country: ':
                country = td_row.text.strip()
            protocols = [Protocol.HTTP]
        return ProxyObject(source=self.id, ip=ip, port=port, anonymity_level=anonymity, country=country, protocols=protocols)

    def __str__(self):
        return "{0} parser of '{1}' with required bandwidth: '{2}' KBs" \
            .format(self.id, self.url, self.minimum_bandwidth_in_KBs)
