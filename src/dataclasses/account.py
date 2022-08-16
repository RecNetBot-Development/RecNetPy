from typing import List

from base import BaseDataClass
from ..misc import date_to_unix, bitmask_decode
from ..misc.api_responses import AccountResponse

PLATFORM_LIST: List[str] = ['Steam', 'Meta', 'PlayStation', 'Xbox', 'RecNet', 'iOS', 'Android', 'Standalone']
PERSONAL_PRONOUNS_LIST: List[str] = ['She / her', 'He / him', 'They / them', 'Ze / hir', 'Ze / zir', 'Xe / xem']
IDENTITY_FLAGS_LIST: List[str] = ['LGBTQIA', 'Transgender', 'Bisexual', 'Lesbian', 'Pansexual', 'Asexual', 'Intersex', 'Genderqueer', 'Nonbinary', 'Aromantic']

class Account(BaseDataClass[AccountResponse]):
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

    def patch_data(self, data: AccountResponse) -> None:
        """
        Sets properties corresponding to data for an api account response.

        @param data: Data from the api.
        """
        self.username = data['username']
        self.display_name = data['displayName']
        self.profile_image = data['profileImage']
        self.is_junior = data['isJunior']
        self.platforms = bitmask_decode(data['platforms'], PLATFORM_LIST)
        self.personal_pronouns = bitmask_decode(data['personalPronouns'], PERSONAL_PRONOUNS_LIST)
        self.identity_flags = bitmask_decode(data['identityFlags'], IDENTITY_FLAGS_LIST)
        self.created_at = date_to_unix(data['createdAt'])