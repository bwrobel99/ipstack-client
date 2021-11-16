from datetime import datetime

from pydantic import BaseModel, Field
from src.helpers.dates import utcnow


class TimestampedModel(BaseModel):
    created_at: datetime = Field(default_factory=utcnow)
    updated_at: datetime = Field(default_factory=utcnow)
