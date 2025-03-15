import sys
from os import environ

from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError, field_validator


class Config(BaseModel):
    DEBUG: bool = False
    DISCORD_BOT_TOKEN: str

    @field_validator("DEBUG", mode="before")
    def convert_str_to_bool(cls, value: str | bool) -> bool:  # noqa: N805
        if isinstance(value, bool):
            return value

        return text_is_true(value)


def text_is_true(text: str) -> bool:
    if text.lower() == "true":
        return True
    if text.lower() == "false":
        return False

    if text.isnumeric():
        return bool(int(text))

    raise ValueError(f"Invalid value: {text}")


load_dotenv()

try:
    environ = {key: value for key, value in environ.items() if value.strip() != ""}
    CONFIG = Config(**environ)  # type: ignore
except ValidationError as errors:
    for error in errors.errors():
        print(f"FATAL: Missing environment variable: {error['loc'][0]}")  # noqa: T201
    sys.exit(1)
