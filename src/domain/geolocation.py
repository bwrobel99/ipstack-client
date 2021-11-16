from typing import Optional

from .base import TimestampedModel


class Geolocation(TimestampedModel):
    ip: str
    continent_code: Optional[str]
    continent_name: Optional[str]
    country_code: Optional[str]
    country_name: Optional[str]
    region_code: Optional[str]
    region_name: Optional[str]
    city: Optional[str]
    zip: Optional[str]
    latitude: Optional[float]
    longitude: Optional[float]
    url: Optional[str] = None

    class Config:
        extra = "ignore"
