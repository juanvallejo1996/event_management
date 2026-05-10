
class UserNotFound(Exception):
    pass


class UserAlreadyExists(Exception):
    pass

class UserInvalidCredentials(Exception):
    pass

class UserUnauthorized(Exception):
    pass

class InvalidEmailFormat(Exception):
    pass

class InvalidPasswordFormat(Exception):
    pass