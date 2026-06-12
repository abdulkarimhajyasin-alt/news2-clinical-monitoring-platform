from __future__ import annotations

import base64
import hashlib
import hmac
import secrets


PBKDF2_ALGORITHM = "pbkdf2_sha256"
PBKDF2_ITERATIONS = 210_000
SALT_BYTES = 16


def hash_password(password: str) -> str:
    salt = secrets.token_bytes(SALT_BYTES)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS)
    return "$".join(
        [
            PBKDF2_ALGORITHM,
            str(PBKDF2_ITERATIONS),
            base64.b64encode(salt).decode("ascii"),
            base64.b64encode(digest).decode("ascii"),
        ]
    )


def verify_password(password: str, password_hash: str) -> bool:
    try:
        algorithm, iterations_text, salt_text, digest_text = password_hash.split("$", 3)
        if algorithm != PBKDF2_ALGORITHM:
            return False
        salt = base64.b64decode(salt_text.encode("ascii"))
        expected = base64.b64decode(digest_text.encode("ascii"))
        actual = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, int(iterations_text))
        return hmac.compare_digest(actual, expected)
    except Exception:
        return False


def is_password_hash_usable(password_hash: str | None) -> bool:
    if not password_hash:
        return False
    try:
        algorithm, iterations_text, salt_text, digest_text = password_hash.split("$", 3)
        if algorithm != PBKDF2_ALGORITHM:
            return False
        iterations = int(iterations_text)
        if iterations <= 0:
            return False
        salt = base64.b64decode(salt_text.encode("ascii"), validate=True)
        digest = base64.b64decode(digest_text.encode("ascii"), validate=True)
        return len(salt) >= SALT_BYTES and len(digest) == hashlib.sha256().digest_size
    except Exception:
        return False
