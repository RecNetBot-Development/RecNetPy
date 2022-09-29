"""
This document contains typed dictionary definitions 
for api responses. It only helps aid with type 
hinting, and serves very little functional purpose.
"""

from distutils.version import Version
from typing import List, Optional, TypedDict

class AccountResponse(TypedDict):
    """
    Typed dictionary used for endpoints that respond with account data.

    Associated endponits:
        - GET https://accounts.rec.net/account/:playerId
        - GET https://accounts.rec.net/account?username={Player_Username}
        - GET https://accounts.rec.net/account/search?name={Search_Query}
        - POST https://accounts.rec.net/account/bulk
    """
    accountId: int
    username: str
    displayName: str
    profileImage: str # Located at https://img.rec.net/:imageName
    isJunior: bool
    platforms: int # Bitmask 2^N = ['Steam', 'Meta', 'PlayStation', 'Xbox', 'RecNet', 'iOS', 'Android', 'Standalone']
    personalPronouns: int # Bitmask 2^N = ['She / her', 'He / him', 'They / them', 'Ze / hir', 'Ze / zir', 'Xe / xem']
    identityFlags: int # Bitmask 2^N = ['LGBTQIA', 'Transgender', 'Bisexual', 'Lesbian', 'Pansexual', 'Asexual', 'Intersex', 'Genderqueer', 'Nonbinary', 'Aromantic']
    createdAt: str

class CommentResponse(TypedDict):
    """
    Typed dictionary for endpoints that respond with comment data.

    Associated endpoints:
        - GET https://api.rec.net/api/images/v1/:photoId/comments
    """
    SavedImageCommentId: int
    SavedImageId: int
    PlayerId: int # Commenter
    Comment: str

class EventResponseResponse(TypedDict):
    """
    Typed dictionary for endpoints that respond with event response data.

    Associated endpoints:
        - GET https://api.rec.net/api/playerevents/v1/:eventId/responses
    """
    PlayerEventResponseId: int
    PlayerEventId: int
    PlayerId: int #Attendee
    CreatedAt: str
    Type: int # 0 = is attending, 1 = may attend, 2 = not attending

class EventResponse(TypedDict):
    """
    Typed dictionary for endpoints that respond with event data.

    Associated endpoints:
        - GET https://api.rec.net/api/playerevents/v1
        - GET https://api.rec.net/api/playerevents/v1/:eventId
        - GET https://api.rec.net/api/playerevents/v1/creator/:playerId
        - GET https://api.rec.net/api/playerevents/v1/search?query={Search_Query}
        - GET https://api.rec.net/api/playerevents/v1/room/:roomId
        - POST https://api.rec.net/api/playerevents/v1/bulk
    """
    PlayerEventId: int
    CreatorPlayerId: int
    ImageName: Optional[str]
    RoomId: int
    SubRoomId: Optional[str]
    ClubId: Optional[str]
    Name: str
    Description: str
    StartTime: str
    EndTime: str
    AttendeeCount: int
    State: int
    Accessibility: int # 0 = private, 1 = public, 2 = unlisted 
    IsMultiInstance: bool
    SupportMultiInstanceChat: bool
    DefaultBroadcastPermissions: int 
    CanRequestBroadcastPermissions: int

class ImageResponse(TypedDict):
    """
    Typed dictionary for endpoints that respond with image data.

    Associated endpoints:
        - GET https://api.rec.net/api/images/v4/:photoId
        - GET https://api.rec.net/api/images/v3/feed/player/:playerId
        - GET https://api.rec.net/api/images/v4/player/:playerId
        - GET https://api.rec.net/api/images/v1/playerevent/:eventId
        - GET https://api.rec.net/api/images/v4/room/:roomId
        - GET https://api.rec.net/api/images/v3/feed/global
        - POST https://api.rec.net/api/images/v3/bulk
    """
    Id: int
    Type: int
    Accessibility: int # 0 = private, 1 = public
    AccessibilityLocked: bool
    ImageName: str
    Description: Optional[str]
    PlayerId: int
    TaggedPlayerIds: List[int]
    RoomId: int
    PlayerEventId: Optional[int]
    CreatedAt: str
    CheerCount: int
    CommentCount: int

class CurrentVersion(TypedDict):
    InventionId: int
    ReplicationId: str
    VersionNumber: int
    BlobName: str
    BlobHash: Optional[str]
    InstantiationCost: int
    LightsCost: int
    ChipsCost: int
    CloudVariablesCost: int

class InventionResponse(TypedDict):
    """
    Typed dictionary for endpoints that respond with invention data.
    Retriving invention data from the api is a relativly new feature,
    so the data structre isn't as well understood compared to other 
    endpoints.

    Associated endpoints:
        - GET https://api.rec.net/api/inventions/v1/featured
        - GET https://api.rec.net/api/inventions/v2/search?value={Search_Query}
        - GET https://api.rec.net/api/inventions/v1/toptoday
        - GET https://api.rec.net/api/inventions/v1?inventionId={Invention_Id}
    """
    InventionId: int
    ReplicationId: str
    CreatorPlayerId: int
    Name: str
    Description: str
    ImageName: str
    CurrentVersionNumber: int
    CurrentVersion: CurrentVersion
    Accessibility: int # 0 = private, 1 = public
    IsPublished: bool
    IsFeatured: bool
    ModifiedAt: str
    CreatedAt: str
    FirstPublishedAt: str
    CreationRoomId: int
    NumPlayersHaveUsedInRoom: int
    NumDownloads: int
    CheerCount: int
    CreatorPermission: int
    GeneralPermission: int
    IsAGInvention: bool
    IsCertifiedInvention: bool
    Price: int
    AllowTrial: bool
    HideFromPlayer: bool

class ProgressionResponse(TypedDict):
    """
    Typed dictionary for endpoints that respond with progression data.

    Associated endpoint:
        - GET https://api.rec.net/api/players/v2/progression/bulk
    """
    PlayerId: int
    Level: int
    XP: int

class Stats(TypedDict):
    CheerCount: int
    FavoriteCount: int
    VisitorCount: int
    VisitCount: int

class SubRoomResponse(TypedDict):
    SupportsJoinInProgress: bool
    UseLevelBasedMatchmaking: bool
    UseAgeBasedMatchmaking: bool
    UseRecRoyaleMatchmaking: bool
    SubRoomId: int
    RoomId: int
    UnitySceneId: str
    Name: str
    DataBlob: str
    DataSavedAt: str
    IsSandbox: bool
    MaxPlayers: int
    Accessibility: int # 0 = private, 1 = public

class RoleResponse(TypedDict):
    AccountId: int
    Role: int # 10 = Member, 20 = Moderator, 30 = Co-owner, 255 = Owner
    LastChangedByAccountId: Optional[int]
    InvitedRole: int

class TagResponse(TypedDict):
    """
    Used for both rooms and inventions.

        - GET https://api.rec.net/api/inventions/v1/details?inventionId={Invention_Id}
    """
    Tag: str
    Type: int # 0 = user submitted, 1 = unknown, 2 = autoadded

class PromoExternalContentResponse(TypedDict):
    Type: int 
    Reference: str # Last part of the url to a youtube video.

class ScoreResponse(TypedDict):
    RoomId: int
    VisitType: int # Unknown, but potentially related to the platforms used.
    Score: int
    BackupScore: Optional[int]

class LoadScreenResponse(TypedDict):
    ImageName: str
    Title: Optional[str]
    Subtitle: Optional[str]

class RoomResponseOptionals(TypedDict, total=False):
    """
    Optional data that can be included in a room data response using
    the 'include' parameter. 

    Include param values:
        - +2 = Subrooms
        - +4 = Roles
        - +8 = Tags
        - +32 = Promotional content
        - +64 = Scores
        - +256 = Loading screens
    """
    SubRooms: List[SubRoomResponse]
    Roles: List[RoleResponse]
    Tags: List[TagResponse]
    PromoImages: List[str]
    PromoExternalContent: List[PromoExternalContentResponse]
    Scores: List[ScoreResponse]
    LoadScreens: List[LoadScreenResponse]

class RoomResponse(RoomResponseOptionals):
    """
    Typed dictionary for endpoints that respond with room data.

    Related endpoints:
        - GET https://rooms.rec.net/rooms/:roomId
        - GET https://rooms.rec.net/rooms?name={Room_Name}
        - GET https://rooms.rec.net/rooms/createdby/:playerId
        - GET https://rooms.rec.net/rooms/ownedby/:playerId
        - GET https://rooms.rec.net/rooms/search?query={Search_Query}
        - GET https://rooms.rec.net/rooms/hot
        - POST https://rooms.rec.net/rooms/bulk
    """
    RoomId: int
    IsDorm: bool
    MaxPlayerCalculationMode: int
    MaxPlayers: int
    CloningAllowed: bool
    DisableMicAutoMute: bool
    DisableRoomComments: bool
    EncryptVoiceChat: bool
    LoadScreenLocked: bool
    Version: int
    Name: str
    Description: str
    ImageName: Optional[str]
    WarningMask: int # Bitmask 2^N = ["Custom", "Spooky/scary themes", "Mature themes", "Bright/flashing lights", "Intense motion", "Gore/violence"]
    CustomWarning: Optional[str]
    CreatorAccountId: int
    State: int
    Accessibility: int # 0 = private, 1 = public
    SupportsLevelVoting: bool
    IsRRO: bool
    SupportsScreens: bool
    SupportsWalkVR: bool
    SupportsTeleportVR: bool
    SupportsVRLow: bool
    SupportsQuest2: bool
    SupportsMobile: bool
    SupportsJuniors: bool
    MinLevel: int
    CreatedAt: str
    Stats: Stats

class FeaturedRoom(TypedDict):
    RoomId: int
    RoomName: str
    ImageName: str

class FeaturedRoomResponse(TypedDict):
    """
    Typed dictionary for the featured room endpoint.

        - GET https://rooms.rec.net/featuredrooms/current
    """
    FeaturedRoomGroupId: int
    Name: str
    StartAt: str
    EndAt: str
    Rooms: List[FeaturedRoom]

class BioResponse(TypedDict):
    """
    Typed dictionary for the bio endpoint.

        - GET https://accounts.rec.net/account/:playerId/bio
    """
    accountId: int
    bio: str

"""
A couple of additonal endpoints are listed below. Most of
These endpoints have return data types that can be easily
expressed using the built in python data types.

Accounts:
    - GET https://clubs.rec.net/subscription/subscribercount/:playerId -> int
    - GET https://api.rec.net/api/influencerpartnerprogram/isinfluencer?accountId={Account_Id} -> bool
    - GET https://api.rec.net/api/influencerpartnerprogram/influencer?accountId={Account_Id} -> int
        (This one doesn't seem to work anymore, but its still called on RecNet.)
Images:
    - GET https://api.rec.net/api/images/v1/:imageId/cheers
"""