from fastapi.security import OAuth2PasswordBearer
from pydantic_settings import BaseSettings

class AuthSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int


auth_settings = AuthSettings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
