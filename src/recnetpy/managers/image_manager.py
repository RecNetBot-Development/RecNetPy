from typing import TYPE_CHECKING, List, Optional

from . import BaseManager
from ..dataclasses import Image

if TYPE_CHECKING:
    from ..misc.api_responses import ImageResponse
    from ..rest import Response

class ImageManager(BaseManager['Image', 'ImageResponse']):
    """
    This is a factory object for creating image objects. Its the
    main interface for fetching image related data.
    """
    async def get(self, name: str) -> Optional['Image']:
        """
        Gets image data by their name, and returns it as an image object.
        Example of an image name: https://img.rec.net/>43ixtpl65wc9fc6ff4vsyrzoo.jpg<
        Only accepts image names of public RecNet posts.
        Returns nothing if the image doesn't exist or is private.
        
        Authorization required.

        :param name: The name of the image.
        :return: An image object representing the data or nothing if not found. 
        """
        data: 'Response[List[ImageResponse]]' = await self.rec_net.images.bulk.name.make_request('post', body = {'Names': name})
        if data.data: return self.create_dataclass(id, data.data[0])
        return None
    
    
    async def get_many(self, names: List[str]) -> List['Image']:
        """
        Gets a list of images by a list of image names, and returns 
        a list of image object.
        Example of an image name: https://img.rec.net/>43ixtpl65wc9fc6ff4vsyrzoo.jpg<
        Only accepts image names of public RecNet posts.
        Images that couldn't be found will be silently ignored.
    
        Authorization required.

        :param name: The name of the image.
        :return: A list of image objects. 
        """
        data: 'Response[List[ImageResponse]]' = await self.rec_net.images.bulk.name.make_request('post', body = {'Names': names})
        return self.create_from_data_list(data.data)
    
    
    async def fetch(self, id: int) -> Optional['Image']:
        """
        Gets image data by their id, and returns it as an image object.
        Returns nothing if the image doesn't exist or is private.

        Authorization required.

        :param id: The id of the image.
        :return: An image object representing the data or nothing if not found. 
        """
        data: 'Response[ImageResponse]' = await self.rec_net.images(id).make_request('get')
        if data.success: return self.create_dataclass(id, data.data)
        return None
    
    
    async def fetch_many(self, ids: List[int]) -> List['Image']:
        """
        Gets a list of images by a list of image ids, and returns 
        a list of image object.
        Images that couldn't be found will be silently ignored.

        Authorization required.

        :param ids: A list of ids.
        :return: A list of image objects. 
        """
        data: 'Response[List[ImageResponse]]' = await self.rec_net.images.bulk.id.make_request('post', body = {'Ids': ids})
        return self.create_from_data_list(data.data)

    async def from_account(self, id: int, take: int = 16, skip: int = 0, sort: int = 0) -> List['Image']:
        """
        Gets a list of images taken by a player.
        If no image or the respective account is found, an empty list will be returned.

        Authorization required.

        :param id: A player id.
        :param take: The number of results to return.
        :param skip: The number of results to skip.
        :param sort: An integer that describes how the results are to be sorted.
        :return: A list of image objects.
        """
        params = {
            'take': take,
            'skip': skip,
            'sort': sort
        }
        data: 'Response[List[ImageResponse]]' = await self.rec_net.images.player(id).make_request('get', params=params)
        return self.create_from_data_list(data.data)

    """
    async def player_feed(self, id: int, take: int = 16, skip: int = 0) -> List['Image']:
        ""
        Gets a list of images taken of a player.
        If no image or the respective account is found, an empty list will be returned.

        Authorization required.

        :param id: A player id.
        :param take: The number of results to return.
        :param skip: The number of results to skip.                 
        :return: A list of image objects.
        ""
        params = {
            'take': take,
            'skip': skip
        }        
        data: 'Response[List[ImageResponse]]' = await self.rec_net.images.feed.player(id).make_request('get', params=params)
        return self.create_from_data_list(data.data)
    """
        
    async def during_event(self, id: int, take: int = 16, skip: int = 0) -> List['Image']:
        """
        Gets a list of images taken during an event.
        If no image or the respective event is found, an empty list will be returned.

        Authorization required.

        :param id: A event id.
        :param take: The number of results to return.
        :param skip: The number of results to skip.
        :return: A list of image objects.
        """
        params = {
            'take': take,
            'skip': skip
        }  
        data: 'Response[List[ImageResponse]]' = await self.rec_net.images.playerevent(id).make_request('get', params=params)
        return self.create_from_data_list(data.data)

    async def in_room(self, id: int, take: int = 16, skip: int = 0, sort: int = 0) -> List['Image']:
        """
        Gets a list of images taken in a room.
        If no image or the respective room is found, an empty list will be returned.

        Authorization required.

        :param id: A room id.
        :param take: The number of results to return.
        :param skip: The number of results to skip.
        :param sort: An integer that describes how the results are to be sorted.
        :return: A list of image objects.
        """
        params = {
            'take': take,
            'skip': skip,
            'sort': sort
        }        
        data: 'Response[List[ImageResponse]]' = await self.rec_net.images.room(id).make_request('get', params=params)
        return self.create_from_data_list(data.data)

    """
    async def front_page(self, take: int = 16, skip: int = 0) -> List['Image']:
        ""
        Gets a list of the most popular images on RecNet.

        Authorization required.

        :param take: The number of results to return.
        :param skip: The number of results to skip.
        :return: A list of image objects.
        ""
        params = {
            'take': take,
            'skip': skip
        }  
        data: 'Response[List[ImageResponse]]' = await self.rec_net.images.feed('global').make_request('get', params=params)
        return self.create_from_data_list(data.data)
    """

    def create_dataclass(self, id: int, data: Optional['ImageResponse'] = None) -> 'Image':
        """
        Creates an image object:

        :param id: An image id.
        :param data: An image api response.
        :return: Returns an image object.
        """
        return Image(self.client, id, data)

    def create_from_data_list(self, data: List['ImageResponse']) -> List['Image']:
        """
        Creates a list of image objects based on a list of data.

        :param data: A list of an image api responses.
        :return: A list of image objects.
        """
        image_list: List['Image'] = []
        for image_data in data:
            image_obj = Image(self.client, image_data['Id'], image_data)
            image_list.append(image_obj)
        return image_list