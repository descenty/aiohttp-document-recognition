import views
from aiohttp.web import Application


def setup_urls(app: Application):
    app.router.add_get('/', views.index)
