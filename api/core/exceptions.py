from distutils.log import info


class CustomizedException(Exception):

    def __init__(self, info):
        self.info = info
        super().__init__(info)

    def __str__(self):
        return self.info


class RegisterNotFound(CustomizedException):
    pass



class ValidationException(CustomizedException):
    pass


class RetryException(CustomizedException):
    pass


class AuthenticationException(CustomizedException):
    pass


class MethodNotImplementedException(CustomizedException):
    pass


class HttpStatusCodeException(CustomizedException):
    pass

