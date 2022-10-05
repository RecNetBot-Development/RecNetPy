class InternalServerError(Exception):
    """
    An exception for a 500 HTTP error.
    """

    def __init__(self):
        message = "Something went wrong within Rec Room's servers. Make sure your input is valid!"
        super().__init__(message)