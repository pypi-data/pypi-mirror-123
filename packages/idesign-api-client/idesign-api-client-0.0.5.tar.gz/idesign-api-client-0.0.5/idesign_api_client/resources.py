import json

from idesign_api_client.utils import urljoin

class ResourcePool:
    def __init__(self, endpoint, session):
        """Initialize the ResourcePool to the given endpoint. Eg: products"""
        self._endpoint = endpoint
        self._session = session

    def get_url(self):
        return self._endpoint

class CreatableResource:
    def create_item(self, item, files=None, params=None):
        if files:
            self._session.headers.pop('Content-Type')
            self._session.headers.pop('Accept')
            print(self._session.headers)
            res = self._session.post(self._endpoint, files=files, data=item, params=params)
        else:
            res = self._session.post(self._endpoint, data=json.dumps(item), params=params)
        return res

class GettableResource:
    def fetch_item(self, code, params=None):
        url = urljoin(self._endpoint, code)
        res = self._session.get(url, params=params)
        return res

class ListableResource:
    def fetch_list(self, params=None):
        res = self._session.get(self._endpoint, params=params)
        return res

class UpdatableResource:
    def update_create_item(self, item, code=None, params=None):
        if code is None:
            code = item.get('id')
        url = urljoin(self._endpoint, code)
        res = self._session.put(url, data=json.dumps(item), params=params)
        return res

class DeletableResource:
    def delete_item(self, code, params=None):
        url = urljoin(self._endpoint, code)
        res = self._session.delete(url, params=params)
        return res

# Pools

# Login
class LoginAccessTokenPool(ResourcePool, CreatableResource):
    def create_item(self, item):
        res = self._session.post(self._endpoint, data=item)
        return res

class LoginPool(ResourcePool):
    
    @property
    def access_token(self):
        return LoginAccessTokenPool(
            urljoin(self._endpoint, 'access-token'), self._session
        )

# User
class UserPool(ResourcePool, ListableResource):
    pass

# Orders
class OrdersDropshippingCostsPool(ResourcePool, CreatableResource):
    pass

class OrdersPool(ResourcePool, GettableResource, ListableResource, CreatableResource):
    
    @property
    def dropshipping_costs(self):
        return OrdersDropshippingCostsPool(
            urljoin(self._endpoint, 'dropshipping-costs'), self._session
        )

# Products
class ProductsDropshippingCostsPool(ResourcePool, ListableResource):
    pass

class ProductsPool(ResourcePool, ListableResource, GettableResource):
    @property
    def dropshipping_costs(self):
        return ProductsDropshippingCostsPool(
            urljoin(self._endpoint, 'dropshipping-costs'), self._session
        )