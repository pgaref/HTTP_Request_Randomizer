from project.http.requests.errors.ParserExceptions import ParserException

class UrlParser(object):
    """
        An abstract class representing any URL containing Proxy information
        To add an extra Proxy URL just implement this class and provide a 'url specific' parse_proxyList method

    Attributes:
        site url (hhtp)
        bandwidth_limit_in_KBs (to remobe straggling proxies when provided by the url)
    """

    def __init__(self, web_url, limitinKBs=None):
        self.url = web_url
        if limitinKBs is not None:
            self.bandwidth_limit_in_KBs=limitinKBs
        else:
            self.bandwidth_limit_in_KBs=150

    def get_URl(self):
        if self.url is None:
            raise ParserException("webURL is NONE")
        return self.url

    def get_bandwidthLimit(self):
        if self.bandwidth_limit_in_KBs <- 0:
            raise ParserException("invalid bandwidth limit {0} ".format(self.bandwidth_limit_in_KBs))
        return self.bandwidth_limit_in_KBs

    def parse_proxyList(self):
        raise ParserException(" abstract method should be implemented by each subclass")

    def __str__(self):
        return "URL Parser of '{0}' with bandwidth limit at '{1}' KBs"\
            .format(self.url, self.bandwidth_limit_in_KBs)