import requests as rq

from idesign_api_client import (
    resources,
    utils
)
from idesign_api_client.config import settings

class IdesignClient:
    def __init__(self, username, password, token=None, api_version='v1', sandbox=False):
        self._session = rq.Session()

        self._username = username
        self._password = password

        self._base_url = utils.urljoin(
            settings.BASE_URL if not sandbox else settings.SANDBOX_BASE_URL, 
            'api', 
            api_version
        )

        self._resources = {
            'login': resources.LoginPool(
                utils.urljoin(self._base_url, 'login'), self._session),
            'user': resources.UserPool(
                utils.urljoin(self._base_url, 'user'), self._session),
            'orders': resources.OrdersPool(
                utils.urljoin(self._base_url, 'orders'), self._session),
            'products': resources.ProductsPool(
                utils.urljoin(self._base_url, 'products'), self._session),
        }        

        self._authenticate(token=token)        


    def _authenticate(self, token=None):
        if not token:
            res = self.login.access_token.create_item({
                'username': self._username,
                'password': self._password
            })
            if res.status_code != 200:
                raise ValueError('Failed to authenticate {}: {}'.format(res.status_code, res.text))
            token = res.json()['access_token']
        
        headers = {
            'Authorization': 'Bearer {}'.format(token)
        }
        self._session.headers.update(headers)

    @property
    def resources(self):
        return self._resources

    @property
    def login(self):
        return self.resources.get('login')

    @property
    def user(self):
        return self.resources.get('user')

    @property
    def orders(self):
        return self.resources.get('orders')

    @property
    def products(self):
        return self.resources.get('products')                        
