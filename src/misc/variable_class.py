from typing import Generic, Type, TypedDict, Optional, List, TypeVar

VC = TypeVar("VC", bound="VariableClass")
RT = TypeVar("RT", bound=TypedDict)

class VariableClass(Generic[RT]):
    """
    This class is ONLY to be inherited. It adds the create_from_list 
    function, but still preserves type safety.
    """
    @classmethod
    def create_from_list(cls: Type[VC], data: Optional[List[RT]] = None) -> Optional[List[VC]]:
        """
        Takes a list of typed dictionaries, and returns them as 
        appropriately typed objects objects. Returns None if data is not provided.

        @param data: A typed dictionary that represenst any Api response.
        @return: Returns a list of VariableClass objects or None. 
        """
        if data is None:
            return None
        object_list: List[VC] = []
        for _, item in enumerate(data):
            object_list.append(cls(item))
        return object_list