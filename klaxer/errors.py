"""Errorz"""

class AuthorizationError(BaseException):
    pass

class NoRouteFoundError(BaseException):
    pass

class ChannelNotFoundError(BaseException):
    pass