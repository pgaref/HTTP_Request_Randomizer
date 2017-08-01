import argparse

import sys

from http_request_randomizer.requests.parsers.FreeProxyParser import FreeProxyParser
from http_request_randomizer.requests.parsers.ProxyForEuParser import ProxyForEuParser
from http_request_randomizer.requests.parsers.RebroWeeblyParser import RebroWeeblyParser
from http_request_randomizer.requests.useragent.userAgent import UserAgentManager


class ProxyList(object):
    def __init__(self):
        self.userAgent = UserAgentManager()
        #####
        # Each of the classes below implements a specific URL Parser
        #####
        self.parsers = list([])
        self.parsers.append(FreeProxyParser('FreeProxy', 'http://free-proxy-list.net'))
        self.parsers.append(ProxyForEuParser('ProxyForEU', 'http://proxyfor.eu/geo.php'))
        self.parsers.append(RebroWeeblyParser('ReBro', 'http://rebro.weebly.com'))

    def get_source_options(self):
        sources = map(lambda x: x.id.lower(), self.parsers)
        sources.append('all')
        return sources


def run(args, proxyList):
    if args.listSources:
        for p in proxyList.parsers:
            print("* id: {0:<30} url: {1:<50}".format(p.id, p.get_url()))


def create_parser(proxyList):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='ProxyList tool retrieving proxies from publicly available providers.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('-ls', '--list',
                       nargs='+',
                       choices=['providers', 'agents'],
                       help='List all available proxy providers sources.',
                       default='providers',
                       required=False)
    group.add_argument('-s', '--sources',
                       nargs='+',
                       choices=proxyList.get_source_options(),
                       help='Use specific proxy provider source.',
                       default='all',
                       required=False)
    parser.add_argument('-o', '--outfile', nargs='?', type=argparse.FileType('w'),
                        metavar='output-file/sys.stdout', default=sys.stdout, required=False)
    return parser


# Wrapper method to satisfy setup.py entry_point
if __name__ == '__main__':
    proxyList = ProxyList()
    parser = create_parser(proxyList)
    parser.parse_args(sys.argv[1:])
    print(parser.args)
    run(parser.args, proxyList)
