class BadRequest(Exception):
    """
    An exception for a 400 HTTP error.
    """

    def __init__(self):
        message = "Bad request, make sure your input is valid!"
        super().__init__(message)