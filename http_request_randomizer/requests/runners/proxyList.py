import argparse
import logging
import sys

import pkg_resources

from http_request_randomizer.requests.parsers.FreeProxyParser import FreeProxyParser
from http_request_randomizer.requests.parsers.ProxyForEuParser import ProxyForEuParser
from http_request_randomizer.requests.parsers.RebroWeeblyParser import RebroWeeblyParser
from http_request_randomizer.requests.parsers.PremProxyParser import PremProxyParser

__author__ = 'pgaref'

handler = logging.StreamHandler()
formatter = logging.Formatter('%(levelname)-8s %(name)-6s %(message)s')
handler.setFormatter(formatter)

logging.getLogger().addHandler(handler)


class ProxyList(object):
    def __init__(self, timeout=1.0, bandwidth=10.0):
        # Each of the entries implements a specific URL Parser
        self.parsers = dict()
        self.parsers['rebro'] = RebroWeeblyParser('ReBro', 'http://rebro.weebly.com', timeout=timeout)
        self.parsers['prem'] = PremProxyParser('Prem', 'https://premproxy.com', timeout=timeout)
        self.parsers['freeproxy'] = FreeProxyParser('FreeProxy', 'http://free-proxy-list.net', timeout=timeout)
        self.parsers['proxyforeu'] = ProxyForEuParser('ProxyForEU', 'http://proxyfor.eu/geo.php',
                                                      bandwidth=bandwidth, timeout=timeout)

    def get_source_options(self):
        sources = list(map(lambda x: x.id.lower(), self.parsers.values()))
        sources.append('all')
        return sources


def run(args):
    # re-initialise with current user settings
    proxy_list = ProxyList(bandwidth=args.bandwidth, timeout=args.timeout)
    # eliminate duplicates
    providers = set(args.source)
    # keep proxy list in memory
    proxy_out = list()
    for source in providers:
        if source == 'all':
            for p in proxy_list.parsers.values():
                print("* id: {0:<30} url: {1:<50}".format(p.id, p.get_url()))
                proxy_out += p.parse_proxyList()
        else:
            p = proxy_list.parsers[source]
            print("* id: {0:<30} url: {1:<50}".format(p.id, p.get_url()))
            proxy_out += p.parse_proxyList()

    # dump proxies to output stream
    for proxy in proxy_out:
        args.outfile.write("{} \n".format(proxy.to_str()))


def create_parser(proxyList):
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description='ProxyList tool retrieving proxies from publicly available providers.')
    parser.add_argument('-s', '--source',
                        nargs='+',
                        choices=proxyList.get_source_options(),
                        dest='source',
                        help='Specify proxy provider(s)',
                        required=True)

    parser.add_argument('-o', '--outfile',
                        nargs='?',
                        type=argparse.FileType('w'),
                        metavar='output-file/sys.stdout',
                        dest='outfile',
                        help='Specify output stream',
                        required=False)
    parser.set_defaults(outfile=sys.stdout)

    parser.add_argument('-t', '--timeout',
                        type=float,
                        dest='timeout',
                        help='Specify provider timeout threshold (seconds)',
                        required=False)
    parser.set_defaults(timeout=1.0)

    parser.add_argument('-bw', '--bandwidth',
                        type=float,
                        dest='bandwidth',
                        help='Specify proxy bandwidth threshold (KBs)',
                        required=False)
    parser.set_defaults(bandwidth=10.0)

    version = pkg_resources.require("http_request_randomizer")[0].version
    parser.add_argument('-v', '--version',
                        action='version',
                        version='%(prog)s {}'.format(version))
    return parser


# Wrapper method to satisfy setup.py entry_point
def main():
    parser = create_parser(ProxyList())
    args = parser.parse_args(sys.argv[1:])
    run(args)
    print("\n All Done \n")


if __name__ == '__main__':
    main()
