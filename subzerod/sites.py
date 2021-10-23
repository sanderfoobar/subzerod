import re
import time
import random
from collections import Counter

from subzerod.utils import EnumBase
import urllib.parse as urlparse


class DuckDuckEnum(EnumBase):
    def __init__(self, domain):
        base_url = 'https://html.duckduckgo.com/html/?q=domain:{q}'
        self.PARAMS = {}
        super(DuckDuckEnum, self).__init__(base_url, domain)

    async def req(self, url, cookies=None):
        try:
            if not self.PARAMS:
                resp = await self.session.get(url, headers=self.headers, timeout=self.timeout)
                resp.raise_for_status()
            else:
                resp = await self.session.post(url, headers=self.headers, timeout=self.timeout, params=self.PARAMS)
                resp.raise_for_status()
        except Exception as e:
            resp = None
        return resp

    async def enumerate(self):
        url = self.base_url.format(q=self.domain)
        while True:
            resp = await self.get_response(await self.req(url))
            if not self.check_response_errors(resp):
                break

            domains = self.extract_domains(resp)
            if not domains:
                break

        await self.session.close()
        return self.subdomains

    def extract_domains(self, resp):
        links_list = []
        link = re.compile('<a rel="nofollow" class="result__a" href="(.*?)">')
        try:
            links_list = link.findall(resp)
            for _link in links_list:
                if _link.startswith("//duck") and "?uddg=" in _link:
                    _link = _link[_link.find('%3A%2F%2F') + 9:]
                    _link = _link[:_link.find('%2F')]
                    _link = f"https://{_link}"
                if not _link.startswith("http"):
                    continue
                subdomain = urlparse.urlparse(_link).netloc
                if subdomain and subdomain not in self.subdomains and subdomain != self.domain and self.domain in subdomain:
                    self.subdomains.append(subdomain.strip())
        except:
            pass

        s = re.compile('<input type="hidden" name="s" value="(.*?)" />')
        next_param = re.compile('<input type="hidden" name="nextParams" value="(.*?)" />')
        v = re.compile('<input type="hidden" name="v" value="(.*?)" />')
        dc = re.compile('<input type="hidden" name="dc" value="(.*?)" />')
        vqd = re.compile('<input type="hidden" name="vqd" value="(.*?)" />')

        try:
            self.PARAMS = {
                "kl": "wt-wt",
                "api": "d.js",
                "o": "json",
                "nextParam": next_param.findall(resp)[0],
                "q": f"domain:{self.domain}",
                "s": s.findall(resp)[0],
                "v": v.findall(resp)[0],
                "dc": dc.findall(resp)[0],
                "vqd": vqd.findall(resp)[0]
            }
        except Exception as ex:
            return
        return links_list

    def check_response_errors(self, resp):
        if not isinstance(resp, str):
            return False
        if "No more results." in resp:
            return False

        return True

    def should_sleep(self):
        return


class CrtEnum(EnumBase):
    def __init__(self, domain):
        base_url = 'https://crt.sh/?q=%25.{domain}'
        super(CrtEnum, self).__init__(base_url, domain)

    async def req(self, url, cookies=None):
        try:
            resp = await self.session.get(url, headers=self.headers, timeout=self.timeout)
        except Exception:
            resp = None

        return await self.get_response(resp)

    async def enumerate(self):
        url = self.base_url.format(domain=self.domain)
        resp = await self.req(url)
        if resp:
            self.extract_domains(resp)
        await self.session.close()
        return self.subdomains

    def extract_domains(self, resp):
        link_regx = re.compile('<TD>(.*?)</TD>')
        try:
            links = link_regx.findall(resp)
            for link in links:
                link = link.strip()
                subdomains = []
                if '<BR>' in link:
                    subdomains = link.split('<BR>')
                else:
                    subdomains.append(link)

                for subdomain in subdomains:
                    if not subdomain.endswith(self.domain) or '*' in subdomain:
                        continue

                    if '@' in subdomain:
                        subdomain = subdomain[subdomain.find('@')+1:]

                    if subdomain not in self.subdomains and subdomain != self.domain:
                        self.subdomains.append(subdomain.strip())
        except Exception as e:
            self.err(e)


class BaiduEnum(EnumBase):
    def __init__(self, domain):
        base_url = 'https://www.baidu.com/s?pn={page_no}&wd={query}&oq={query}'
        self.MAX_DOMAINS = 2
        self.MAX_PAGES = 760
        super(BaiduEnum, self).__init__(base_url, domain)
        self.querydomain = self.domain

    def extract_domains(self, resp):
        links = list()
        found_newdomain = False
        subdomain_list = []
        link_regx = re.compile('<a.*?class="c-showurl".*?>(.*?)</a>')
        try:
            links = link_regx.findall(resp)
            for link in links:
                link = re.sub('<.*?>|>|<|&nbsp;', '', link)
                if not link.startswith('http'):
                    link = "http://" + link
                subdomain = urlparse.urlparse(link).netloc
                if subdomain.endswith(self.domain):
                    subdomain_list.append(subdomain)
                    if subdomain not in self.subdomains and subdomain != self.domain:
                        found_newdomain = True
                        self.subdomains.append(subdomain.strip())
        except Exception:
            pass
        if not found_newdomain and subdomain_list:
            self.querydomain = self.findsubs(subdomain_list)
        return links

    def findsubs(self, subdomains):
        count = Counter(subdomains)
        subdomain1 = max(count, key=count.get)
        count.pop(subdomain1, "None")
        subdomain2 = max(count, key=count.get) if count else ''
        return (subdomain1, subdomain2)

    async def check_response_errors(self, resp):
        return True

    def should_sleep(self):
        time.sleep(random.randint(2, 5))
        return

    def generate_query(self):
        if self.subdomains and self.querydomain != self.domain:
            found = ' -site:'.join(self.querydomain)
            query = "site:{domain} -site:www.{domain} -site:{found} ".format(domain=self.domain, found=found)
        else:
            query = "site:{domain} -site:www.{domain}".format(domain=self.domain)
        return query


class AskEnum(EnumBase):
    def __init__(self, domain):
        base_url = 'https://www.ask.com/web?o=0&l=dir&qo=serpSearchTopBox&q={query}'
        self.MAX_DOMAINS = 15
        self.MAX_PAGES = 5
        super(AskEnum, self).__init__(base_url, domain)
        self.headers['User-Agent'] = "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36"

    def extract_domains(self, resp):
        links_list = list()
        link_regx = re.compile("[a-zA-Z.]+\.nu\.nl")
        try:
            links_list = link_regx.findall(resp)
            for link in links_list:
                if not link.startswith("http"):
                    link = f"https://{link}"
                if f"www.{self.domain}" in link:
                    continue

                subdomain = urlparse.urlparse(link).netloc
                if subdomain not in self.subdomains and subdomain != self.domain:
                    self.subdomains.append(subdomain.strip())
        except:
            pass

        return links_list

    def get_page(self, num):
        return num + 1

    def generate_query(self):
        fmt = 'site:{domain} -www.{domain}'
        q = fmt.format(domain=self.domain)
        for domain in self.subdomains:
            q += f" -{domain}"
        return q


class ThreatCrowd(EnumBase):
    def __init__(self, domain):
        base_url = 'https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}'
        super(ThreatCrowd, self).__init__(base_url, domain)

    async def enumerate(self):
        url = self.base_url.format(domain=self.domain)
        async with self.session.get(url) as resp:
            blob = await resp.json()
            if "subdomains" in blob and isinstance(blob['subdomains'], list):
                self.subdomains = blob['subdomains']

        await self.session.close()
        return self.subdomains


class PassiveDNS(EnumBase):
    def __init__(self, domain):
        base_url = 'https://api.sublist3r.com/search.php?domain={domain}'
        super(PassiveDNS, self).__init__(base_url, domain)

    async def enumerate(self):
        url = self.base_url.format(domain=self.domain)
        async with self.session.get(url) as resp:
            blob = await resp.json()
            if isinstance(blob, list):
                self.subdomains = blob
        await self.session.close()
        return self.subdomains


class DomainLookup(EnumBase):
    """Discover domains on a shared IP"""
    def __init__(self, ip_address):
        base_url = "https://api.mnemonic.no/pdns/v3/search"
        super(DomainLookup, self).__init__(base_url, ip_address)

    async def enumerate(self):
        params = {
            "customerID": [],
            "rrType": [],
            "tlp": [],
            "rrClass": [],
            "offset": 0,
            "limit": 1000,
            "includeAnonymousResults": True,
            "aggregateResult": True,
            "query": self.domain
        }

        resp = await self.session.post(self.base_url, json=params)
        resp = await resp.json()

        for entry in resp.get('data', []):
            if "query" in entry:
                self.subdomains.append(entry['query'])

        await self.session.close()
        return self.subdomains
