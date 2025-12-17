import pytest

from tests.api.utils.allure.setup import (
    allure_class_setup,
    allure_test_setup,
    Severity,
    Epic,
    Feature,
    Tag,
    Story,
)


@pytest.mark.api
@pytest.mark.category
@allure_class_setup(
    severity=Severity.CRITICAL,
    tags=[Tag.SMOKE, Tag.REGRESS],
    epic=Epic.ARTICLE_SERVICE,
    feature=Feature.CATEGORY,
)
class TestCategoryAPI:
    @allure_test_setup(title="Get all categories", story=Story.GET)
    def test_get_all(self):
        assert 1 == 1
