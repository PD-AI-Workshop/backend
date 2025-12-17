import allure
import asyncio
import functools
from typing import List
from enum import StrEnum


class Severity(StrEnum):
    TRIVIAL = "Trivial"
    MINOR = "Minor"
    MAJOR = "Major"
    CRITICAL = "Critical"
    BLOCKER = "Blocker"


class Tag(StrEnum):
    SMOKE = "Smoke"
    REGRESS = "Regress"
    NEGATIVE = "Negative"


class Epic(StrEnum):
    USER_SERVICE = "User service"
    ARTICLE_SERVICE = "Article service"


class Feature(StrEnum):
    AUTH = "Auth"
    CATEGORY = "Category"
    USER = "User"
    FILE = "File"
    Article = "Article"


class Story(StrEnum):
    LOGIN = "Login"
    CREATE = "Create resource"
    GET = "Get resource"
    UPDATE = "Update resource"
    DELETE = "Delete resource"


def allure_class_setup(
    severity: Severity,
    tags: List[Tag],
    epic: Epic,
    feature: Feature,
):
    def decorator(cls):
        for dec in (
            allure.severity(severity),
            allure.tag(*tags),
            allure.epic(epic),
            allure.feature(feature),
            allure.parent_suite(epic),
            allure.suite(feature)
        ):
            cls = dec(cls)
        return cls
    return decorator


def allure_test_setup(title: str, story: Story):
    def decorator(func):
        decorated_func = allure.story(story)(func)
        decorated_func = allure.sub_suite(story)(decorated_func)
        decorated_func = allure.title(title)(decorated_func)

        if asyncio.iscoroutinefunction(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                return await decorated_func(*args, **kwargs)
        else:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return decorated_func(*args, **kwargs)
        return wrapper
    return decorator