class ResourceException(Exception):

    def __init__(self, message):
        super().__init__(message)


class AuthException(Exception):
    def __init__(self, reason=''):
        if reason != '':
            super().__init__(reason)
        super().__init__('invalid token')


