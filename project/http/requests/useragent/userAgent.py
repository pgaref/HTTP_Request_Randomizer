import random

class UserAgent:

    def __init__(self, web_proxy_list=[]):
        self.agent_file = '../data/user_agents.txt'
        self.useragents = self.load_user_agents(self.agent_file)

    def load_user_agents(self, useragentsfile):
        """
        useragentfile : string
            path to text file of user agents, one per line
        """
        useragents = []
        with open(useragentsfile, 'rb') as uaf:
            for ua in uaf.readlines():
                if ua:
                    useragents.append(ua.strip()[1:-1-1])
        return useragents

    def random_user_agent(self):
        """
        useragents : string array of different user agents
        :param useragents:
        :return random agent:
        """
        user_agent = random.choice(self.useragents)
        return user_agent

    def first_user_agent(self):
        return self.useragents[0]

    def last_user_agent(self):
        return self.useragents[-1]

    def len_user_agent(self):
        return len(self.useragents)


if __name__ == '__main__':

    ua = UserAgent()
    print "Number of User Agent headers: " + str(ua.len_user_agent) 
    print "First User Agent in file: " + ua.first_user_agent()
    print "Last User Agent in file: " + ua.last_user_agent()
    print "If you want one random header for a request, you may use the following header:\n"
    print "User-Agent: " + ua.random_user_agent() + "\n"

