from typing import TYPE_CHECKING, List, Optional, Dict

from .base import BaseDataClass
from .comment import Comment
from ..misc import date_to_unix
from ..misc.constants import ACCESSIBILITY_DICT

if TYPE_CHECKING:
    from . import Account, Room, Event
    from ..misc.api_responses import ImageResponse, CommentResponse, AccountResponse
    from ..rest import Response

IMAGE_TYPE: Dict[int, str] = {
    0: None,
    1: "Share Camera",
    2: "Outfit Thumbnail",
    3: "Room Thumbnail",
    4: "Profile Thumbnail",
    5: "Invention Thumbnail",
    6: "Player Event Thumbnail",
    7: "Room Load Screen"
}

class Image(BaseDataClass['ImageResponse']):
    """
    This class represents a RecNet image.
    """

    #: This is an image's unique identifier.
    id: int
    #: This is the type of image which has the possible value of ``[None, 'Share Camera', 'Outfit Thumbnail', 'Room Thumbnail', 'Profile Thumbnail', 'Invention Thumbnail', 'Player Event Thumbnail', 'Room Load Screen']``.
    #type: str
    #: This is the visibilty of the image which has the possible value of ``['Private', 'Public', 'Unlisted']``.
    #accessibility: str
    #: This is true if the accessiblity of the image is fixed, false if its able to able to be changed.
    #accessibility_locked: bool
    #: This is the file name of the image itself.
    image_name: str
    #: This is the description of the image.
    description: Optional[str]
    #: This is the id of the player who took the image.
    player_id: int
    #: This is a list of player id's who were tagged in the image.
    tagged_player_ids: List[int]
    #: This is the id of the room the image was taken it.
    room_id: Optional[int]
    #: This is the event the image was taken during.
    event_id: Optional[int]
    #: This is the date the image was taken on represented as an Unix integer.
    created_at: int
    #: This is the number of cheers the image has recieved.
    cheer_count: int
    #: This is the number of comments the post has recieved.
    comment_count: int
    #: This is an account object representing the player who took the image.
    player: Optional['Account'] = None
    #: This is a list of account objects that represent the player who can be seen in the image.
    tagged_players: Optional[List['Account']] = None
    #: This is a room object which represents the room the image was taken in.
    room: Optional['Room'] = None
    #: This is an event object which represents the event the image was taken during.
    event: Optional['Event'] = None
    #: This is a list of player ids who cheered the image.
    cheer_player_ids: Optional[List[int]] = None
    #: This is a list of comment objects that represent comments left on the image.
    comments: Optional[List['Comment']] = None
    #: This is a list of account objects that represents players who cheered the image.
    cheer_players: Optional[List['Account']] = None

    def patch_data(self, data: 'ImageResponse') -> None:
        """
        Sets properties corresponding to data for an api event response.

        :param data: Data from the api.
        """
        self.data = data
        self.id = data['Id']
        #self.type = IMAGE_TYPE.get(data['Type'], "Unknown")
        #self.accessibility = ACCESSIBILITY_DICT.get(data['Accessibility'], "Unknown")
        #self.accessibility_locked = data['AccessibilityLocked']
        self.image_name = data['ImageName']
        self.description = data['Description']
        self.player_id = data['PlayerId']
        #self.tagged_player_ids = data['TaggedPlayerIds']
        self.tagged_player_ids = []
        self.room_id = data['RoomId']
        self.event_id = data['PlayerEventId']
        self.created_at = date_to_unix(data['CreatedAt'], new=False)
        self.cheer_count = data['CheerCount']
        self.comment_count = data['CommentCount']

    async def get_player(self, force: bool = False) -> 'Account':
        """
        Fetches the creator of the image. Returns a
        cached result, if this function has been already called.

        :param force: If true, fetches new data.
        :return: An account object.
        """
        if self.player is None or force:
            self.player = await self.client.accounts.fetch(self.player_id)
        return self.player

    async def get_tagged_players(self, force: bool = False) -> List['Account']:
        """
        Fetches account data for the player who appeared in the Image. Returns a
        cached result, if this function has been already called.

        :param force: If true, fetches new data.
        :return: A list of account objects.
        """
        if not self.tagged_player_ids: return []
        if self.tagged_players is None or force:
            self.tagged_players = await self.client.accounts.fetch_many(self.tagged_player_ids)
        return self.tagged_players

    async def get_room(self, include: int = 0, force: bool = False) -> 'Room':
        """
        Fetches the room the image was taked in. Returns a
        cached result, if this function has been already called.

        | Include param values:

        ===== ===================
        Value Resolve
        ===== ===================
        2     Subrooms
        4     Roles
        8     Tags
        32    Promotional content
        64    Scores
        256   Loading screens
        ===== ===================

        :param force: If true, fetches new data.
        :return: A room object.
        """
        if self.room_id is None: return None
        if self.room is None or force:
            self.room = await self.client.rooms.fetch(self.room_id, include)
        return self.room

    async def get_event(self, force: bool = False) -> Optional['Event']:
        """
        Fetches the event the image was taken in. Returns a
        cached result, if this function has been already called.

        :param force: If true, fetches new data.
        :return: An event object, or None if the image wasn't taken in an event.
        """
        if self.event_id is None: return None
        if self.event is None or force:
            self.event = await self.client.events.fetch(self.event_id)
        return self.event
        
    async def get_cheers(self, force: bool = False) -> List[int]:
        """
        Fetches a list of players' ids who cheered the post. Returns a
        cached result, if this function has been already called.

        :param force: If true, fetches new data.
        :return: A list of account ids.
        """        
        if self.cheer_count == 0: return []
        if self.cheer_player_ids is None or force:
            data: 'Response[List[int]]' = await self.rec_net.images(self.id).cheers.make_request('get')
            self.cheer_player_ids = data.data           
        return self.cheer_player_ids

    async def get_comments(self, force: bool = False) -> List['Comment']:
        """
        Fetches a list of comments made on the image. Returns a
        cached result, if this function has been already called.

        :param force: If true, fetches new data.
        :return: An list of comment objects.
        """
        if self.comment_count == 0: return []
        if self.comments is None or force:
            data: 'Response[List[CommentResponse]]' = await self.rec_net.images(self.id).comments.make_request('get')
            self.comments = Comment.create_from_list(data.data)
        return self.comments

    async def resolve_cheers(self, force: bool = False) -> List['Account']:
        """
        Fetches a list of player objects who cheered the post. Returns a
        cached result, if this function has been already called.

        :param force: If true, fetches new data.
        :return: A list of account objects.
        """ 
        if not self.cheer_player_ids: return []
        if self.cheer_players is None or force:
            player_ids = await self.get_cheers(force)
            self.cheer_players = await self.client.accounts.fetch_many(player_ids)
        return self.cheer_players

    async def resolve_commenters(self, force: bool = False) -> List['Comment']:
        """
        Resolves the players who commented on an image. This function
        will make an api call every time its used. It should only be used when 
        updating the comment player attribute.

        :param force: Forces new responses to be fetched.
        :return: A list of comment objects. 
        """
        if self.comment_count == 0: return []
        if self.comments is None or force:
            comments = await self.get_comments(force)
            players: Dict[int, Account] = {}
            for comment in comments:
                player = self.client.accounts.create_dataclass(comment.player_id)
                comment.player = player
                players[comment.player_id] = player
            data: 'Response[List[AccountResponse]]' = await self.rec_net.accounts.bulk.make_request('post', body = {id: players.keys})
            for data_response in data.data: players.get(data_response['accountId']).patch_data(data_response)
        return self.comments
