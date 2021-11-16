import hashlib
from src.settings import Settings


settings = Settings()
ALGORITHM = "sha256"
ITERATIONS = 100000


def hash_password(plain_password: str) -> str:
    return hashlib.pbkdf2_hmac(
        ALGORITHM,
        plain_password.encode("utf-8"),
        settings.PASSWORD_HASH_SALT.encode("utf-8"),
        ITERATIONS,
    ).hex()


def compare_password_with_hash(plain_password: str, hash: str) -> bool:
    return hash_password(plain_password) == hash
