from typing import TYPE_CHECKING, Optional

from ..misc import VariableClass

if TYPE_CHECKING:
    from . import Account, Image
    from ..misc.api_responses import CommentResponse


class Comment(VariableClass['CommentResponse']):
    """
    This class represents a comment left under an image.
    """

    #: This is a comments unique identifier.
    saved_image_comment_id: int
    #: This is the id of the image the comment was left under.
    saved_image_id: int
    #: This is the id of the player who created the comment.
    player_id: int
    #: This is the comment made on the image.
    comment: str
    #: This is a player object the represents the player who create the comment.
    player: Optional['Account']

    def __init__(self, data: 'CommentResponse') -> None:
        self.saved_image_comment_id = data['SavedImageCommentId']
        self.saved_image_id = data['SavedImageId']
        self.player_id = data['PlayerId']
        self.comment = data['Comment']