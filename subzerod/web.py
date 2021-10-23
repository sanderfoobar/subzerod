from aiohttp import web
import urllib.parse as urlparse

from subzerod import SubZerod
from subzerod.utils import validate_ip

routes = web.RouteTableDef()


@routes.get('/scan/{inp}')
async def inp(request):
    host = request.match_info.get("inp", "")
    if not host:
        return web.Response(text="no")

    if not validate_ip(host):
        if not host.startswith('http://') or not host.startswith('https://'):
            host = f"http://{host}"
        host = urlparse.urlparse(host).netloc
        results = await SubZerod.find_subdomains(host)
        results.insert(0, host)
    else:
        results = await SubZerod.find_domains(host)

    return web.json_response(results)


def run_web():
    app = web.Application()
    app.add_routes(routes)
    web.run_app(app, host="0.0.0.0", port=9342)
