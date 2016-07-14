from project.http.requests.parsers.UrlParser import UrlParser
import requests
from bs4 import BeautifulSoup


class freeproxyParser(UrlParser):

    def __init__(self, web_url):
        UrlParser.__init__(self, web_url)

    def parse_proxyList(self):
        curr_proxy_list = []
        content = requests.get(self.get_URl()).content
        soup = BeautifulSoup(content, "html.parser")
        table = soup.find("table", attrs={"class": "display fpltable"})

        # The first tr contains the field names.
        headings = [th.get_text() for th in table.find("tr").find_all("th")]

        datasets = []
        for row in table.find_all("tr")[1:]:
            dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
            datasets.append(dataset)

        for dataset in datasets:
            # Check Field[0] for tags and field[1] for values!
            proxy = "http://"
            for field in dataset:
                if field[0] == 'IP Address':
                    proxy = proxy + field[1] + ':'
                elif field[0] == 'Port':
                    proxy = proxy + field[1]
            curr_proxy_list.append(proxy.__str__())
            # print "{0:<10}: {1}".format(field[0], field[1])
        # print "ALL: ", curr_proxy_list
        return curr_proxy_list

    def __str__(self):
        return "FreeProxy Parser of '{0}' with bandwidth limit at '{1}' KBs" \
            .format(self.url, self.bandwidth_limit_in_KBs)

