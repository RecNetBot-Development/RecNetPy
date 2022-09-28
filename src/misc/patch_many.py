from abc import ABC, abstractmethod
from typing import Dict, Generic, List, TypedDict, TypeVar

from ..dataclasses import BaseDataClass

def patch_many(obj_dict: Dict[int, BaseDataClass], data: List[Dict], id_key: str):
        """
        Takes a dictionary with ids being the keys and dataclasses 
        as the items, and fetch and patches data to the objects.
        
        @param obj_dict: A dictionary of dataclasses
        @param id_key: The key of the id in the response.
        """
        for _, item in data:
            obj = obj_dict.get(item[id_key])
            obj.patch_data(item)