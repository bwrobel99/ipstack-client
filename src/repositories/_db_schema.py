from sqlalchemy import Column, DateTime, MetaData, String, Table, UniqueConstraint
from sqlalchemy.sql.sqltypes import Float, Integer

metadata = MetaData(schema="schema")

GEOLOCATION_IP_UNIQUE_CONSTRAINT = "geolocation_ip_unique_constraint"
GEOLOCATION_URL_UNIQUE_CONSTRAINT = "geolocation_url_unique_constraint"

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("username", String(length=255), nullable=False, unique=True),
    Column("password_hash", String(length=255), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
)

geolocation = Table(
    "geolocation",
    metadata,
    Column("id", Integer, primary_key=True, nullable=False),
    Column("ip", String(length=20), nullable=False),
    Column("url", String(length=255), unique=True),
    Column("continent_code", String(length=5)),
    Column("continent_name", String(length=255)),
    Column("country_code", String(length=5)),
    Column("country_name", String(length=255)),
    Column("region_code", String(length=5)),
    Column("region_name", String(length=255)),
    Column("city", String(length=255)),
    Column("zip", String(length=10)),
    Column("latitude", Float),
    Column("longitude", Float),
    Column("created_at", DateTime(timezone=True), nullable=False),
    Column("updated_at", DateTime(timezone=True), nullable=False),
    UniqueConstraint("ip", name=GEOLOCATION_IP_UNIQUE_CONSTRAINT),
    UniqueConstraint("url", name=GEOLOCATION_URL_UNIQUE_CONSTRAINT),
)
