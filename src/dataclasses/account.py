from typing import TYPE_CHECKING, List, Optional

from .base import BaseDataClass
from .progression import Progression
from ..misc import date_to_unix, bitmask_decode

if TYPE_CHECKING:
    from . import Event, Image, Room
    from ..misc.api_responses import AccountResponse, ProgressionResponse, BioResponse
    from ..rest import Response


PLATFORM_LIST: List[str] = ['Steam', 'Meta', 'PlayStation', 'Xbox', 'RecNet', 'iOS', 'Android', 'Standalone']
PERSONAL_PRONOUNS_LIST: List[str] = ['She / her', 'He / him', 'They / them', 'Ze / hir', 'Ze / zir', 'Xe / xem']
IDENTITY_FLAGS_LIST: List[str] = ['LGBTQIA', 'Transgender', 'Bisexual', 'Lesbian', 'Pansexual', 'Asexual', 'Intersex', 'Genderqueer', 'Nonbinary', 'Aromantic']

class Account(BaseDataClass['AccountResponse']):
    """
    This dataclass represents a RecNet account. 
    """
    username: str
    display_name: str
    profile_image: str
    is_junior: bool
    platforms: List[str]
    personal_pronouns: List[str]
    identity_flags: List[str]
    created_at: int
    bio: Optional[str] = None
    level: Optional[Progression] = None
    subscriber_count: Optional[int] = None
    is_influencer: Optional[bool] = None
    events: Optional[List['Event']] = None
    created_rooms: Optional[List['Room']] = None
    owned_rooms: Optional[List['Room']] = None
    images: Optional[List['Image']] = None
    feed: Optional[List['Image']] = None


    def patch_data(self, data: 'AccountResponse') -> None:
        """
        Sets properties corresponding to data for an api account response.

        @param data: Data from the api.
        """
        self.data = data
        self.username = data['username']
        self.display_name = data['displayName']
        self.profile_image = data['profileImage']
        self.is_junior = data['isJunior']
        self.platforms = bitmask_decode(data['platforms'], PLATFORM_LIST)
        self.personal_pronouns = bitmask_decode(data['personalPronouns'], PERSONAL_PRONOUNS_LIST)
        self.identity_flags = bitmask_decode(data['identityFlags'], IDENTITY_FLAGS_LIST)
        self.created_at = date_to_unix(data['createdAt'])

    async def get_events(self, take: int = 16, skip: int = 0, force: bool = False) -> List['Event']:
        """
        Fetches a list of events made by this player. Returns a
        cached result, if this function has been already called.

        @param take: The number of results to return.
        @param skip: The number of results to skip.
        @param force: If true, fetches new data.
        @return: A list of events.
        """
        if self.events is None or force:
            self.events = await self.client.events.from_account(self.id, take, skip)
        return self.events

    async def get_images(self, take: int = 16, skip: int = 0, sort: int = 0, force: bool = False) -> List['Image']:
        """
        Fetches a list of images taken by this player. Returns a
        cached result, if this function has been already called.

        @param take: The number of results to return.
        @param skip: The number of results to skip.
        @param sort: An integer that describes how the results are to be sorted.
        @param force: If true, fetches new data.
        @return: A list of images.
        """
        if self.images is None or force:
            self.images = await self.client.images.from_account(self.id, take, skip, sort)
        return self.images

    async def get_feed(self, take: int = 16, skip: int = 0, force: bool = False) -> List['Image']:
        """
        Fetches a list of images taken of this player. Returns a
        cached result, if this function has been already called.

        @param take: The number of results to return.
        @param skip: The number of results to skip.
        @param force: If true, fetches new data.
        @return: A list of images.
        """
        if self.feed is None or force:
            self.feed = await self.client.images.player_feed(self.id, take, skip)
        return self.feed

    async def get_created_rooms(self, force: bool = False) -> List['Room']:
        """
        Fetches a list of rooms created by this player. Returns a
        cached result, if this function has been already called.

        @param force: If true, fetches new data.
        @return: A list of rooms.
        """
        if self.created_rooms is None or force:
            self.created_rooms = await self.client.rooms.created_by(self.id)
        return self.created_rooms

    async def get_owned_rooms(self, force: bool = False) -> List['Room']:
        """
        Fetches a list of rooms owned by this player. Returns a
        cached result, if this function has been already called.

        @param force: If true, fetches new data.
        @return: A list of rooms.
        """
        if self.owned_rooms is None or force:
            self.owned_rooms = await self.client.rooms.owned_by(self.id)
        return self.owned_rooms

    async def get_bio(self, force: bool = False) -> str:
        """
        Fetches this player's bio. Returns a
        cached result, if this function has been already called.

        @param force: If true, fetches new data.
        @return: The player's bio.
        """
        if self.bio is None or force:
            data: 'Response[BioResponse]' = await self.rec_net.accounts.account(self.id).bio.make_request('get')
            self.bio = data.data['bio']
        return self.bio

    async def get_level(self, force: bool = False) -> 'Progression':
        """
        Fetches this player's level as a progression object. Returns a
        cached result, if this function has been already called.

        @param force: If true, fetches new data.
        @return: This player's level.
        """
        if self.level is None or force:
            data: 'Response[List[ProgressionResponse]]' = await self.rec_net.api.players.v2.progression.bulk.make_request('post', body = {'id': [self.id]})
            self.level = Progression(data.data[0])
        return self.level

    async def get_subscriber_count(self, force: bool = False) -> int:
        """
        Fetches this players subscriber count. Returns a
        cached result, if this function has been already called.

        @param force: If true, fetches new data.
        @return: This player's subscriber count.
        """
        if self.subscriber_count is None or force:
            data: 'Response[int]' = await self.rec_net.clubs.subscription.subscribercount(self.id).make_request('get')
            self.subscriber_count = data.data
        return self.subscriber_count

    async def get_is_influencer(self, force: bool = False) -> bool:
        """
        Fetches whether this player is an influencer. Returns a
        cached result, if this function has been already called.

        @param force: If true, fetches new data.
        @return: This player's subscriber count.
        """
        if self.is_influencer is None or force:
            data: 'Response[bool]' = await self.rec_net.api.influencerpartnerprogram.isinfluencer.make_request('get', params = {'accountId': self.id})
            self.is_influencer = data.data
        return self.is_influencer 