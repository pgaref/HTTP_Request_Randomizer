import logging

import requests
from bs4 import BeautifulSoup

from http_request_randomizer.requests.parsers.UrlParser import UrlParser
from http_request_randomizer.requests.proxy.ProxyObject import ProxyObject, AnonymityLevel

logger = logging.getLogger(__name__)
__author__ = 'pgaref'


# Samair Proxy now renamed to: premproxy.com
class SamairProxyParser(UrlParser):
    def __init__(self, id, web_url, timeout=None):
        web_url += "/list/"
        UrlParser.__init__(self, id, web_url, timeout)

    def parse_proxyList(self):
        curr_proxy_list = []
        try:
            # Parse all proxy pages -> format: /list/{num}.htm
            # Get the pageRange from the 'pagination' table
            page_set = self.get_pagination_set()
            logger.debug("Pages: {}".format(page_set))
            for page in page_set:
                response = requests.get("{0}{1}".format(self.get_url(), page), timeout=self.timeout)
                if not response.ok:
                    # Could not parse ANY page - Let user know
                    if not curr_proxy_list:
                        logger.warn("Proxy Provider url failed: {}".format(self.get_url()))
                    # Return proxies parsed so far
                    return curr_proxy_list
                content = response.content
                soup = BeautifulSoup(content, "html.parser")
                # css provides the port number so we reverse it
                # for href in soup.findAll('link'):
                #     if '/styles/' in href.get('href'):
                #         style = "http://www.samair.ru" + href.get('href')
                #         break
                # css = requests.get(style).content.split('\n')
                # css.pop()
                # ports = {}
                # for l in css:
                #     p = l.split(' ')
                #     key = p[0].split(':')[0][1:]
                #     value = p[1].split('\"')[1]
                #     ports[key] = value

                table = soup.find("div", attrs={"id": "proxylist"})
                # The first tr contains the field names.
                headings = [th.get_text() for th in table.find("tr").find_all("th")]
                for row in table.find_all("tr")[1:]:
                    td_row = row.find("td")
                    # curr_proxy_list.append('http://' + row.text + ports[row['class'][0]])
                    proxy_obj = self.create_proxy_object(row)
                    # Make sure it is a Valid Proxy Address
                    if proxy_obj is not None and UrlParser.valid_ip_port(td_row.text):
                        curr_proxy_list.append(proxy_obj)
                    else:
                        logger.debug("Proxy Invalid: {}".format(td_row.text))
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
            logger.warn("Proxy Provider url failed: {}".format(self.get_url()))
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

    def create_proxy_object(self, row):
        for td_row in row.findAll("td"):
            if td_row.attrs['data-label'] == 'IP:port ':
                text = td_row.text.strip()
                ip = text.split(":")[0]
                # Make sure it is a Valid IP
                if not UrlParser.valid_ip(ip):
                    logger.debug("IP with Invalid format: {}".format(ip))
                    return None
                port = text.split(":")[1]
            elif td_row.attrs['data-label'] == 'Anonymity Type: ':
                anonymity = AnonymityLevel.get(td_row.text.strip())
            elif td_row.attrs['data-label'] == 'Country: ':
                country = td_row.text.strip()
        return ProxyObject(source=self.id, ip=ip, port=port, anonymity_level=anonymity, country=country)

    def __str__(self):
        return "SemairProxy Parser of '{0}' with required bandwidth: '{1}' KBs" \
            .format(self.url, self.minimum_bandwidth_in_KBs)