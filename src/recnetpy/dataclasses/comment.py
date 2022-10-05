from typing import TYPE_CHECKING, Optional

from ..misc import VariableClass

if TYPE_CHECKING:
    from . import Account, Image
    from ..misc.api_responses import CommentResponse


class Comment(VariableClass['CommentResponse']):
    """
    This class represents a comment left under an image.
    """
    saved_image_comment_id: int
    saved_image_id: int
    player_id: int
    comment: str
    saved_image: 'Image'
    player: Optional['Account']

    def __init__(self, data: 'CommentResponse') -> None:
        self.saved_image_comment_id = data['SavedImageCommentId']
        self.saved_image_id = data['SavedImageId']
        self.player_id = data['PlayerId']
        self.comment = data['Comment']