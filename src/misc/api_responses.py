"""
This document contains typed dictionary deffintions 
for api responses. It only helps aid with type 
hinting, and serves very little functional purpose.
"""

from typing import TypedDict


class AccountResponse(TypedDict):
    accountId: int
    username: str
    displayName: str
    profileImage: str
    isJunior: bool
    platforms: int
    personalPronouns: int
    createdAt: str

class CommentResponse(TypedDict):
    SavedImageCommentId: int
    SavedImageId: int
    PlayerId: int
    Comment: str

class EventResponseResponse(TypedDict):
    PlayerEventResponseId: int
    PlayerEventId: int
    PlayerId: int
    CreatedAt: str
    Type: int

class EventResponse(TypedDict):
    PlayerEventId: int
    CreatorPlayerId: int
    ImageName: str
    RoomId: int
    SubRoomId: int
    ClubId: int
    Name: str
    Description: str
    StartTime: str
    EndTime: str
    AttendeeCount: int
    State: int
    Accessibility: int
    IsMultiInstance: bool
    SupportMultiInstanceChat: bool
    DefaultBroadcastPermissions: int
    CanRequestBroadcastPermissions: int

class ImageResponse(TypedDict):
    pass