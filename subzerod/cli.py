import sys

import urllib.parse as urlparse

from subzerod import SubZerod
from subzerod.utils import validate_ip


async def cli(host: str):
    if not validate_ip(host):
        if not host.startswith('http://') or not host.startswith('https://'):
            host = f"http://{host}"
        host = urlparse.urlparse(host).netloc
        results = await SubZerod.find_subdomains(host)
        results.insert(0, host)
        for domain in results:
            print(urlparse.unquote(domain))
    else:
        results = await SubZerod.find_domains(host)
        for domain in results:
            print(domain)


def cli_run():
    import asyncio
    try:
        arg = sys.argv[1]
    except:
        print(f"Usage: ./{sys.argv[0]} <domain name or IPv4 address>")
        sys.exit(1)

    if arg == "web":
        from subzerod.web import run_web
        run_web()
    else:
        asyncio.run(cli(arg))
