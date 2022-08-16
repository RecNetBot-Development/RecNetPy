from abc import ABC, abstractmethod
from typing import Dict, Generic, List, TypedDict, TypeVar

from ..dataclasses import BaseDataClass

BDC = TypeVar("BDC", bound=BaseDataClass)
RT = TypeVar("RT", bound=TypedDict)

class PatchMany(ABC, Generic[BDC, RT]):
    """
    This Class is ONLY to be inherited. It adds the patch_many 
    fuction to a manager class. bulk_fetch_data is required to
    be defined.  
    """
    @abstractmethod
    async def bulk_fetch_data(self, ids: List[int]) -> List[RT]:
        pass

    async def patch_many(self, obj_dict: Dict[int, BDC], id_key: str) -> None:
        """
        Takes a dictionary with ids being the keys and dataclasses 
        as the items, and fetch and patches data to the objects.
        
        @param obj_dict: A dictionary of dataclasses
        @param id_key: The key of the id in the response.
        @return: None
        """
        data = await self.bulk_fetch_data(obj_dict.keys)
        for _, item in data:
            obj = obj_dict.get(item[id_key])
            obj.patch_data(item)