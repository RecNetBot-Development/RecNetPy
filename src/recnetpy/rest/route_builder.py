from typing import TYPE_CHECKING, List, Dict, Optional

from .request import Request

if TYPE_CHECKING:
    from .http_client import HTTPClient
    from .response import Response

class RouteBuilder:
    """
    A builder class used to construct routes
    to be sent as requests.
    """
    route: List[str]
    base: str
    client: 'HTTPClient'
    use_auth: bool
  
    def __init__(self, client: 'HTTPClient', base: str, use_auth: bool = False) -> None:
        self.route = []
        self.base = base
        self.client = client
        self.use_auth = use_auth

    async def make_request(self, method: str, params: Optional[Dict] = None, body: Optional[Dict] = None, headers: Optional[Dict] = {}, api_version: str = "v1") -> 'Response':
        """
        Joins the route components into a url, and constructs
        a request object that is processed by the http client.

        @param method: The method used to sent the request.
        @param params: The url params used in the request.
        @param body: The body of the request.
        @return: The response from the request.
        """
        if self.use_auth:
            if headers is None: headers = {}
            headers['Ocp-Apim-Subscription-Key'] = self.client.api_key
        headers["Api-Version"] = api_version
        #headers["Content-Type"] = "application/x-www-form-urlencoded"
        url = self.base + "/".join(self.route)
        request = Request(self.client.session, method, url, params, body, headers)
        return await self.client.push(request)

    def __getattr__(self, name: str):
        """
        Appends the requested attribute to the route 
        component list, and returns a self referense.

        @param name: The name of the object attrubute. 
        """
        self.route.append(name)
        return self

    def __call__(self, *args):
        """
        Converts the arguments passed into a call to
        the object into strings, and adds them to
        the route component list. Returns a self
        reference.
        """
        self.route += [*map(str, args)]
        return self