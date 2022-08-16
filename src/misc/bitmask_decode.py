from typing import List

def bitmask_decode(bitmask: int, resolved_list: List[str]) -> List[str]:
    """
    Decodes a bitmasked integer into a human readable list of items.

    @param bitmask: Bitmasked integer to be decoded.
    @param resolved_list: A list where each item coresponds to the state of the next base two place value.
    @return: A list of items the bitmask resolved to. 
    """
    decoded_list: List[str] = []
    for index, item in enumerate(resolved_list):
        if 1 << index & bitmask:
            decoded_list.append(item)
    return decoded_list