import os
import random
from fake_useragent import FakeUserAgent
import logging

logger = logging.getLogger(__name__)

class UserAgentManager:
    def __init__(self, fallback=None, file=None):
        self.agent_file = file
        if file is not None:
            logger.info('Using local file for user agents: '+self.agent_file)
            self.useragents = self.load_user_agents(self.agent_file)
        else:
            logger.info('Using fake-useragent package for user agents.')
            fb = fallback
            self.fakeuseragent = FakeUserAgent(fallback=fb)

    def load_user_agents(self, useragentsfile):
        """
        useragentsfile : string
            path to text file of user agents, one per line
        """
        useragents = []
        with open(useragentsfile, 'rb') as uaf:
            for ua in uaf.readlines():
                if ua:
                    useragents.append(ua.strip()[1:-1 - 1])
        return useragents

    def get_random_user_agent(self):
        if self.agent_file:
            user_agent = random.choice(self.useragents)
            return user_agent.decode('utf-8')
        else:
            return self.fakeuseragent.random

    def get_first_user_agent(self):
        if self.agent_file:
            return self.useragents[0].decode('utf-8')
        else:
            logger.warning('User-Agents file not set')
            return None

    def get_last_user_agent(self):
        if self.agent_file:
            return self.useragents[-1].decode('utf-8')
        else:
            logger.warning('User-Agents file not set')
            return None

    def get_len_user_agent(self):
        if self.agent_file:
            return len(self.useragents)
        else:
            logger.warning('User-Agents file not set')
            return None


if __name__ == '__main__':
    ua = UserAgentManager()
    if ua.agent_file:
        print("Number of User Agent headers: {0}".format(ua.get_len_user_agent()))
        print("First User Agent in file: {0}".format(ua.get_first_user_agent()))
        print("Last User Agent in file: {0}".format(ua.get_last_user_agent()))
    else:
        print("Using up-to-date user agents from online databse.")
    print("If you want one random header for a request, you may use the following header:\n")
    print("User-Agent: " + ua.get_random_user_agent() + "\n")
