import re
import requests
import logging

logger = logging.getLogger(__name__)


class JsUnPacker(object):
    """
    It takes the javascript file's url which contains the port numbers for
    the encrypted strings. The file has to be unpacked to a readable form just like
    http://matthewfl.com/unPacker.html does. Then we create a dictionary for
    every key:port pair.
    """
    # TODO: it might not be necessary to unpack the js code

    def __init__(self, js_file_url):
        logger.info("JS UnPacker init path: {}".format(js_file_url))
        r = requests.get(js_file_url)
        encrypted = r.text.strip()
        encrypted = '(' + encrypted.split('}(')[1][:-1]
        unpacked = eval('self.unpack' +encrypted) # string of the js code in unpacked form
        matches = re.findall(r".*?\('\.([a-zA-Z0-9]{1,6})'\).*?\((\d+)\)", unpacked)
        self.ports = dict((key, port) for key, port in matches)
        logger.debug('portmap: '+str(self.ports))

    def baseN(self, num, b, numerals="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"):
        return ((num == 0) and numerals[0]) or (self.baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

    def unpack(self, p, a, c, k, e=None, d=None):
        while c:
            c -= 1
            if k[c]:
                p = re.sub("\\b" + self.baseN(c, a) + "\\b",  k[c], p)
        return p

    def get_port(self, key):
        return self.ports[key]

    def get_ports(self):
        return self.ports
