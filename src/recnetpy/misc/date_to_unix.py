from datetime import datetime

def date_to_unix(date: str) -> int:
    """
    Converts dates from RecNet to an unix timestamp, that can be used to show dates more elegantly.

    Credit to Jegarde for this function.

    @param date: String representation of a date.
    @return: Unix date represented as an integer.
    """
        
    timestamp = datetime.strptime(date, '%m/%d/%Y %H:%M:%S %p').timestamp()
        
    return int(timestamp)  # Return UNIX timestamp