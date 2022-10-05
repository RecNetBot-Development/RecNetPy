from typing import Any, List

def stringify_bulk(bulk: List[Any]) -> List[str]:
    """
    Stringifies each element in a bulk meant for a request to prevent possible invalid inputs.
    """
    return list(map(lambda ele: str(ele), bulk))