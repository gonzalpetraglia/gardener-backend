
class EndpointException(Exception):

    def __init__(self):
        self.message = "internal_error"
        self.status_code = 500


class UserNotFound(EndpointException):

    def __init__(self):
        self.message = "user_not_found"
        self.status_code = 400


class IncorrectPassword(EndpointException):

    def __init__(self):
        self.message = "password_not_matching"
        self.status_code = 400


class ProviderNotImplemented(EndpointException):

    def __init__(self):
        self.message = "provider_unavailable"
        self.status_code = 400
