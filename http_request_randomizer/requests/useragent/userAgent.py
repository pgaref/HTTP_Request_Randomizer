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
            if fallback is None:
                fallback = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
            self.fakeuseragent = FakeUserAgent(fallback=fallback, cache=False)

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
            logger.warning('Fake-useragent library does not support operaration get_first - change to user-agent file!')
            return None

    def get_last_user_agent(self):
        if self.agent_file:
            return self.useragents[-1].decode('utf-8')
        else:
            logger.warning('Fake-useragent library does not support operaration get_last - change to user-agent file!')
            return None

    def get_len_user_agent(self):
        if self.agent_file:
            return len(self.useragents)
        else:
            logger.warning('Fake-useragent library does not support operaration get_len - change to user-agent file!')
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
