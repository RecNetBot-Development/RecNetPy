class NotFound(Exception):
    """
    An exception for a 404 HTTP error.
    """

    def __init__(self):
        message = "The data you were looking for can't be found! It either doesn't exist or is private."
        super().__init__(message)