from typing import TYPE_CHECKING, List, Optional, Dict

from .base import BaseDataClass
from .comment import Comment
from ..misc import date_to_unix
from ..misc.constants import ACCESSIBILITY_DICT

if TYPE_CHECKING:
    from . import Account, Room, Event
    from ..misc.api_responses import ImageResponse, CommentResponse, AccountResponse
    from ..rest import Response

class Image(BaseDataClass['ImageResponse']):
    """
    This class represents a RecNet image.
    """
    id: int
    type: int
    accessibility: str
    accessibility_locked: bool
    image_name: str
    description: Optional[str]
    player_id: int
    tagged_player_ids: List[int]
    room_id: int
    player_event_id: Optional[int]
    created_at: int
    cheer_count: int
    comment_count: int
    player: Optional['Account'] = None
    tagged_players: Optional[List['Account']] = None
    room: Optional['Room'] = None
    player_event: Optional['Event'] = None
    cheer_player_ids: Optional[List[int]] = None
    comments: Optional[List['Comment']] = None
    cheer_players: Optional[List['Account']] = None

    def patch_data(self, data: 'ImageResponse') -> None:
        """
        Sets properties corresponding to data for an api event response.

        @param data: Data from the api.
        """
        self.data = data
        self.id = data['Id']
        self.type = data['Type']
        self.accessibility = ACCESSIBILITY_DICT.get(data['Accessibility'], "Unknown")
        self.accessibility_locked = data['AccessibilityLocked']
        self.image_name = data['ImageName']
        self.description = data['Description']
        self.player_id = data['PlayerId']
        self.tagged_player_ids = data['TaggedPlayerIds']
        self.room_id = data['RoomId']
        self.player_event_id = data['PlayerEventId']
        self.created_at = date_to_unix(data['CreatedAt'])
        self.cheer_count = data['CheerCount']
        self.comment_count = data['CommentCount']

    async def get_player(self, force: bool = False) -> 'Account':
        """
        Fetches the creator of the image. Returns a
        cached result, if this function has been already called.

        @param force: If true, fetches new data.
        @return: An account object.
        """
        if self.player is None or force:
            self.player = await self.client.accounts.fetch(self.player_id)
        return self.player

    async def get_tagged_players(self, force: bool = False) -> List['Account']:
        """
        Fetches account data for the player who appeared in the Image. Returns a
        cached result, if this function has been already called.

        @param force: If true, fetches new data.
        @return: A list of account objects.
        """
        if self.tagged_players is None or force:
            self.tagged_players = await self.client.accounts.fetch_many(self.tagged_player_ids)
        return self.tagged_players

    async def get_room(self, force: bool = False) -> 'Room':
        """
        Fetches the room the image was taked in. Returns a
        cached result, if this function has been already called.

        @param force: If true, fetches new data.
        @return: A room object.
        """
        if self.room is None or force:
            self.room = await self.client.rooms.fetch(self.room_id)
        return self.room

    async def get_player_event(self, force: bool = False) -> Optional['Event']:
        """
        Fetches the event the image was taken in. Returns a
        cached result, if this function has been already called.

        @param force: If true, fetches new data.
        @return: An event object, or None if the image wasn't taken in an event.
        """
        if self.player_event_id is None: return None
        if self.player_event is None or force:
            self.player_event = await self.client.events.fetch(self.player_event_id)
        return self.player_event
        
    async def get_cheers(self, force: bool = False) -> List[int]:
        """
        Fetches a list of players' ids who cheered the post. Returns a
        cached result, if this function has been already called.

        @param force: If true, fetches new data.
        @return: A list of account ids.
        """        
        if self.cheer_player_ids is None or force:
            data: 'Response[List[int]]' = await self.rec_net.api.images.v1(self.id).cheers.make_request('get')
            self.cheer_player_ids = data.data           
        return self.cheer_player_ids

    async def get_comments(self, force: bool = False) -> List['Comment']:
        """
        Fetches a list of comments made on the image. Returns a
        cached result, if this function has been already called.

        @param force: If true, fetches new data.
        @return: An list of comment objects.
        """
        if self.comments is None or force:
            data: 'Response[List[CommentResponse]]' = await self.rec_net.api.images.v1(self.id).comments.make_request('get')
            self.comments = Comment.create_from_list(data.data)
        return self.comments

    async def resolve_cheers(self, force: bool = False) -> List['Account']:
        """
        Fetches a list of player objects who cheered the post. Returns a
        cached result, if this function has been already called.

        @param force: If true, fetches new data.
        @return: A list of account objects.
        """  
        if self.cheer_players is None or force:
            player_ids = await self.get_cheers(force)
            self.cheer_players = self.client.accounts.fetch_many(player_ids)
        return self.cheer_players

    async def resolve_commenters(self, force: bool = False) -> List['Comment']:
        """
        Resolves the players who commented on an image. This function
        will make an api call every time its used. It should only be used when 
        updating the comment player attribute.

        @param force: Forces new responses to be fetched.
        @return: A list of comment objects. 
        """
        if self.comments is None or force:
            comments = await self.get_comments(force)
            players: Dict[int, Account] = {}
            for comment in comments:
                player = self.client.accounts.create_dataclass(comment.player_id)
                comment.player = player
                players[comment.player_id] = player
            data: 'Response[List[AccountResponse]]' = await self.rec_net.accounts.account.bulk.make_request('post', body = {id: players.keys})
            for data_response in data.data: players.get(data_response['accountId']).patch_data(data_response)
        return self.comments
