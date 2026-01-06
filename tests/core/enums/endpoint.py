from enum import StrEnum


class ResourceEndpoint(StrEnum):
    CATEGORY = "/categories/"
    AUTH = "/auth/"
    USER = "/user/"
    TEST = "/test/"
