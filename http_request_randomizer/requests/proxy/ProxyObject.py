from enum import Enum


class ProxyObject(object):
    def __init__(self, source, ip, port, anonymity_level, country=None,  protocols=[], tunnel=False):
        """ Proxy object implementation - base for all the parsing logic

        :param source: The name of the proxy list from which the proxy was collected
        :param ip: The IP address of the proxy
        :param port: The port number of the proxy
        :param anonymity_level: The anonymity level of the proxy. Can be any of :AnonymityLevel
        :param country: Alpha-2 country code of the country in which the proxy is geo-located
        :param protocols:  A list of protocols that the proxy supports. May contain one or more of {HTTP, HTTPS, SOCKS5, SOCKS6}
        :param tunnel: Whether or not the proxy supports tunneling to HTTPS target URLs.
        """
        self.source = source
        self.ip = ip
        self.port = port
        self.anonymity_level = anonymity_level
        self.country = country
        self.protocols = protocols
        self.tunnel = tunnel

    def get_address(self):
        return "{0}:{1}".format(self.ip, self.port)

    def __str__(self):
        """ Method is heavily used for Logging - make sure we have a readable output

        :return: The address representation of the proxy
        """
        return "{0} | {1}".format(self.get_address(), self.source)

    def to_str(self):
        return "Address: {0} | Src: {1} | | Country: {2} | Anonymity: {3} | Protoc: {4} | Tunnel: {5}"\
            .format(self.get_address(), self.source, self.country, self.anonymity_level, self.protocols,
                    self.tunnel)


# class AnonymityEnumMeta(EnumMeta):
#     def __call__(cls, value, *args, **kw):
#         if isinstance(value, str):
#             # map string Alias to enum values, defaults to Unknown
#             value = {
#                 'transparent': 1,
#                 'transparent proxy': 1,
#                 'LOW': 1,
#                 'anonymous': 2,
#                 'anonymous proxy': 2,
#                 'high-anonymous': 2,
#                 'elite': 3,
#                 'elite proxy': 3,
#                 'HIGH': 3
#             }.get(value, 0)
#         return super(AnonymityEnumMeta, cls).__call__(value, *args, **kw)


class AnonymityLevel(Enum):
    # __metaclass__ = AnonymityEnumMeta
    """
    UNKNOWN: The proxy anonymity capabilities are not exposed
    TRANSPARENT: The proxy does not hide the requester's IP address.
    ANONYMOUS: The proxy hides the requester's IP address, but adds headers to the forwarded request that make it clear
        that the request was made using a proxy.
    ELITE: The proxy hides the requester's IP address and does not add any proxy-related headers to the request.
    """
    UNKNOWN = 0   # default
    TRANSPARENT = 1, 'transparent', 'transparent proxy', 'LOW'
    ANONYMOUS = 2, 'anonymous', 'anonymous proxy', 'high-anonymous'
    ELITE = 3, 'elite', 'elite proxy', 'HIGH', 'Elite & Anonymous'

    def __new__(cls, int_value, *value_aliases):
        obj = object.__new__(cls)
        obj._value_ = int_value
        for alias in value_aliases:
            cls._value2member_map_[alias] = obj
        return obj

    @classmethod
    def get(cls, name):
        try:
            return cls(name)
        except ValueError:
            return cls.UNKNOWN

class Protocol(Enum):
    UNKNOWN = 0
    HTTP = 1
    HTTPS = 2
    SOCS4 = 3
    SOCS5 = 4
