import allure
from typing import Any
from jsonschema import validate
from jsonschema.validators import Draft202012Validator

from tests.core.utils.logger import get_logger

logger = get_logger("JSON SCHEMA VALIDATOR")


@allure.step("Validate JSON-schema")
def validate_json_schema(response: Any, schema: dict) -> None:
    logger.info("Validate JSON-schema")

    validate(
        schema=schema,
        instance=response,
        format_checker=Draft202012Validator.FORMAT_CHECKER,
    )
