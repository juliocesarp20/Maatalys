import logging

import bcrypt

logger = logging.getLogger(__name__)


class PasswordManager:
    @staticmethod
    def hash_password(password: str) -> str:
        logger.debug("Hashing password.")
        salt = bcrypt.gensalt(rounds=12)
        return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        logger.debug("Verifying password.")
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
