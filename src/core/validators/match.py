"""Validator models for all successful responses or unsuccessful."""

import pydantic


class Match(pydantic.BaseModel):
    """**Match model."""

    result: bool = True
    email: str | None = None
    model_config = pydantic.ConfigDict(title="Match model")
