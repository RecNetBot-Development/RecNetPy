from typing import List, Optional

from . import BaseManager
from ..dataclasses import Image
from ..misc.api_responses import ImageResponse
from ..rest import Response

class ImageManager(BaseManager[Image, ImageResponse]):
    async def fetch(self, id: int) -> Image:
        """
        Gets image data by their id, and returns it as an image object.

        @param id: The id of the image.
        @return: An image object representing the data. 
        """
        data: Response[ImageResponse] = await self.rec_net.api.images.v4(id).make_request('get')
        return self.create_dataclass(id, data.data)

    async def fetch_many(self, ids: List[int]) -> List[Image]:
        """
        Gets a list of images by a list of image ids, and returns 
        a list of image object.

        @param ids: A list of ids.
        @return: A list of image objects. 
        """
        data: Response[List[ImageResponse]] = await self.rec_net.api.images.v3.bulk.make_request('get', body = {'id': ids})
        return self.create_from_data_list(data.data)

    async def from_account(self, id: int) -> List[Image]:
        """
        Gets a list of images taken by a player.

        @param query: A player id.
        @return: A list of image objects.
        """
        data: Response[List[ImageResponse]] = await self.rec_net.api.images.v4.player(id).make_request('get')
        return self.create_from_data_list(data.data)

    async def player_feed(self, id: int) -> List[Image]:
        """
        Gets a list of images taken of a player.

        @param query: A player id.
        @return: A list of image objects.
        """
        data: Response[List[ImageResponse]] = await self.rec_net.api.images.v3.feed.player(id).make_request('get')
        return self.create_from_data_list(data.data)

    async def during_event(self, id: int) -> List[Image]:
        """
        Gets a list of images taken during an event.

        @param query: A event id.
        @return: A list of image objects.
        """
        data: Response[List[ImageResponse]] = await self.rec_net.api.images.v1.playerevent(id).make_request('get')
        return self.create_from_data_list(data.data)

    async def in_room(self, id: int) -> List[Image]:
        """
        Gets a list of images taken in a room.

        @param query: A room id.
        @return: A list of image objects.
        """
        data: Response[List[ImageResponse]] = await self.rec_net.api.images.v4.room(id).make_request('get')
        return self.create_from_data_list(data.data)

    async def front_page(self) -> List[Image]:
        """
        Gets a list of the most popular images on RecNet.

        @return: A list of image objects.
        """
        data: Response[List[ImageResponse]] = await self.rec_net.api.images.v3.feed('global').make_request('get')
        return self.create_from_data_list(data.data)

    def create_dataclass(self, id: int, data: Optional[ImageResponse] = None) -> Image:
        """
        Creates an image object:

        @param id: An image id.
        @param data: An image api response.
        @return: Returns an image object.
        """
        return Image(self.client, id, data)

    def create_from_data_list(self, data: List[ImageResponse]) -> List[Image]:
        """
        Creates a list of image objects based on a list of data.

        @param data: A list of an image api responses.
        @return: A list of image objects.
        """
        image_list: List[Image] = []
        for image_data in data:
            image_obj = Image(self.client, image_data['Id'], image_data)
            image_list.append(image_obj)
        return image_list