from aiohttp import web
from urls import setup_urls


app = web.Application()
setup_urls(app)

if __name__ == '__main__':
    web.run_app(app)