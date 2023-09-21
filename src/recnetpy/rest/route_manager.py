from .route_builder import RouteBuilder
from .http_client import HTTPClient

class RouteManager:
    """
    This class serves as a factory for route
    builder objects. Also helps serve as a
    facade for all the other underlying classes.
    """
    client: HTTPClient

    def __init__(self, api_key: str):
        self.client = HTTPClient(api_key)

    @property
    def apim(self) -> RouteBuilder:
        """
        Creates a route builer with a base url
        for apim endpoint requests.

        @return: A apim route builder.
        """
        return RouteBuilder(self.client, "https://apim.rec.net/public/", use_auth=True)
    
    @property
    def api(self) -> RouteBuilder:
        """
        Creates a route builer with a base url
        for api endpoint requests.

        @return: A api route builder.
        """
        return RouteBuilder(self.client, "https://api.rec.net/api/", use_auth=True)

    @property
    def events(self) -> RouteBuilder:
        """
        Creates a route builer with a base url
        for event endpoint requests.

        @return: An events route builder.
        """
        return RouteBuilder(self.client, "https://apim.rec.net/public/playerevents/", use_auth=True)

    @property
    def images(self) -> RouteBuilder:
        """
        Creates a route builer with a base url
        for images endpoint requests.

        @return: An images route builder.
        """
        return RouteBuilder(self.client, "https://apim.rec.net/public/images/", use_auth=True)

    @property
    def rooms(self) -> RouteBuilder:
        """
        Creates a route builer with a base url
        for rooms endpoint requests.

        @return: A rooms route builder.
        """
        return RouteBuilder(self.client, "https://apim.rec.net/public/rooms/", use_auth=True)

    @property
    def accounts(self) -> RouteBuilder:
        """
        Creates a route builer with a base url
        for accounts endpoint requests.

        @return: A accounts route builder.
        """
        return RouteBuilder(self.client, "https://apim.rec.net/public/accounts/", use_auth=True)

    @property
    def clubs(self) -> RouteBuilder:
        """
        Creates a route builer with a base url
        for clubs endpoint requests.

        @return: A clubs route builder.
        """
        return RouteBuilder(self.client, "https://clubs.rec.net/")

    @property
    def cdn(self) -> RouteBuilder:
        """
        Creates a route builer with a base url
        for cdn endpoint requests.

        @return: A cdn route builder.
        """
        return RouteBuilder(self.client, "https://cdn.rec.net/")

    @property
    def namespace(self) -> RouteBuilder:
        """
        Creates a route builer with a base url
        for ns endpoint requests.

        @return: A namespace route builder.
        """
        return RouteBuilder(self.client, "https://ns.rec.net/")

    def custom(self, host: str) -> RouteBuilder:
        """
        Creates a route builer with a base url
        for cutom endpoint requests.

        @return: A cutome route builder.
        """
        return RouteBuilder(self.client, host)

    async def stop(self) -> None:
        """
        Safely ends the underlying client.
        """
        await self.client.stop()