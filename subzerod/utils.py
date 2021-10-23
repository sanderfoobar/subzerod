import re
import sys
import socket
from random import choice, randrange

from subzerod.agents import user_agents

import aiohttp


accepts = [
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
]


class EnumBase(object):
    def __init__(self, base_url, domain):
        self.MAX_DOMAINS = 40
        self.MAX_PAGES = 10
        self.domain = domain
        self.session = aiohttp.ClientSession()
        self.timeout = 5
        self.subdomains = []
        self.base_url = base_url
        self.headers = {
            'User-Agent': choice(user_agents),
            'Accept': choice(accepts),
            'Accept-Language': choice(f"en-US,en;q=0.{randrange(4, 9)}"),
            'Accept-Encoding': 'gzip',
            'Cache-Control': 'no-cache',
            'Pragma': 'no-cache'
        }

    async def send_req(self, query, page_no=1):
        url = self.base_url.format(query=query, page_no=page_no)
        try:
            resp = await self.session.get(url, headers=self.headers, timeout=self.timeout)
        except Exception:
            resp = None
        return await self.get_response(resp)

    async def get_response(self, response):
        if response is None:
            return 0
        return await response.text()

    def check_max_subdomains(self, count):
        if self.MAX_DOMAINS == 0:
            return False
        return count >= self.MAX_DOMAINS

    def check_max_pages(self, num):
        if self.MAX_PAGES == 0:
            return False
        return num >= self.MAX_PAGES

    # override
    def extract_domains(self, resp):
        """ child class should override this function """
        return

    # override
    async def check_response_errors(self, resp):
        """ child class should override this function
        The function should return True if there are no errors and False otherwise
        """
        return True

    def should_sleep(self):
        """Some enumerators require sleeping to avoid bot detections like Google enumerator"""
        return

    def generate_query(self):
        """ child class should override this function """
        return

    def get_page(self, num):
        """ child class that user different pagination counter should override this function """
        return num + 10

    def err(self, msg):
        sys.stderr.write((str(f"[-] {self.__class__.__name__} {msg}\n")))

    async def enumerate(self):
        flag = True
        page_no = 0
        prev_links = []
        retries = 0

        while flag:
            # finding the number of subdomains found so far
            query = self.generate_query()
            count = query.count(self.domain)

            # if they we reached the maximum number of subdomains
            # in search query then we should go over the pages
            if self.check_max_subdomains(count):
                page_no = self.get_page(page_no)

            # maximum pages for Google to avoid getting blocked
            if self.check_max_pages(page_no):
                await self.session.close()
                return self.subdomains
            resp = await self.send_req(query, page_no)

            # check if there is any error occured
            if not await self.check_response_errors(resp):
                await self.session.close()
                return self.subdomains
            links = self.extract_domains(resp)

            # if the previous page hyperlinks was the similar to the current one,
            # then maybe we have reached the last page
            if links == prev_links:
                retries += 1
                page_no = self.get_page(page_no)

                # make another retry maybe it isn't the last page
                if retries >= 3:
                    await self.session.close()
                    return self.subdomains

            prev_links = links
            self.should_sleep()

        await self.session.close()
        return self.subdomains


def validate_domain(domain: str):
    # validate domain
    domain_check = re.compile("^(http|https)?[a-zA-Z0-9]+([\-\.]{1}[a-zA-Z0-9]+)*\.[a-zA-Z]{2,}$")
    if not domain_check.match(domain):
        return False
    return True


def validate_ip(addr: str):
    try:
        socket.inet_aton(addr)
        return True
    except socket.error:
        return False
