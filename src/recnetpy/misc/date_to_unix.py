from datetime import datetime
from dateutil.parser import isoparse

def date_to_unix(date: str, new: bool = False) -> int:
    """
    Converts dates from RecNet to an unix timestamp, that can be used to show dates more elegantly.

    Credit to Jegarde for this function.

    @param date: String representation of a date.
    @param new: Use the new date type
    @return: Unix date represented as an integer.
    """
        
    if new:
        timestamp = datetime.strptime(date, '%m/%d/%Y %H:%M:%S %p').timestamp()
    else:
        timestamp = isoparse(date).timestamp()
        
    return int(timestamp)  # Return UNIX timestamp