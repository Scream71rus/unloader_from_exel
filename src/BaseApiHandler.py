
import requests
from urllib.parse import urljoin


class BaseApiHandler(requests.Session):
    def __init__(self, base_uri=None, email="", token="", *args, **kwargs):
        super(BaseApiHandler, self).__init__(*args, **kwargs)
        if not base_uri:
            raise Exception("You must provide at least base uri")

        self.prefix_url = base_uri

        self.headers = BaseApiHandler.make_headers(email, token)

    def request(self, method, url, *args, **kwargs):
        url = urljoin(self.prefix_url, url)
        return super(BaseApiHandler, self).request(method, url, *args, **kwargs)

    @staticmethod
    def make_headers(email, token):
        return {
            'User-Agent': 'App/1.0 (%s)' % email,
            'Authorization': token,
        }
