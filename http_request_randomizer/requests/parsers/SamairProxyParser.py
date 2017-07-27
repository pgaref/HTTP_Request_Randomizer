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
        # Parse all proxy pages -> format: /list/{num}.htm
        # TODO @pgaref: get the pageRange from the 'pagination' table
        for page in range(1, 21):
            response = requests.get("{0}{num:02d}.htm".format(self.get_URl(), num=page), timeout=self.timeout)
            if not response.ok:
                # Could not parse ANY page - Let user know
                if not curr_proxy_list:
                    logger.warn("Proxy Provider url failed: {}".format(self.get_URl()))
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
                # Make sure it is a Valid Proxy Address
                if UrlParser.valid_ip_port(td_row.text):
                    proxy_obj = self.createProxyObject(row)
                    proxy_obj.print_everything()
                    curr_proxy_list.append(proxy_obj)
                else:
                    logger.debug("Address with Invalid format: {}".format(td_row.text))
        return curr_proxy_list

    def createProxyObject(self, row):
        for td_row in row.findAll("td"):
            if td_row.attrs['data-label'] == 'IP:port ':
                ip = td_row.text.split(":")[0]
                port = td_row.text.split(":")[1]
            elif td_row.attrs['data-label'] == 'Anonymity Type: ':
                anonymity = AnonymityLevel(td_row.text)
            elif td_row.attrs['data-label'] == 'Country: ':
                country = td_row.text
        return ProxyObject(source=self.id, ip=ip, port=port, anonymity_level=anonymity, country=country)

    def __str__(self):
        return "SemairProxy Parser of '{0}' with required bandwidth: '{1}' KBs" \
            .format(self.url, self.minimum_bandwidth_in_KBs)
