class ProxyObject(object):

    def __int__(self, ip_address, port, anonymity_level, country):
        self.ip_address = ip_address
        self.port = port
        self.anonymity_level = anonymity_level
        self.country = country

    def print_everything(self):
        print("Address: {0} | Port: {1} | Country: {2} | Anonymity: {3}" \
              .format(self.ip_address, self.port, self.country, self.anonymity_level))
