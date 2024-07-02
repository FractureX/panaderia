import os
import json
from pydantic_settings import BaseSettings

def get_env_filename():
    runtime_env = os.getenv("ENV")
    return f".env.{runtime_env}" if runtime_env else ".env"

class EnvironmentSettings(BaseSettings):
    API_VERSION: str
    APP_NAME: str
    DATABASE_HOSTNAME: str | dict[str, str]
    DATABASE_NAME: str | dict[str, str]
    DATABASE_PASSWORD: str | dict[str, str]
    DATABASE_PORT: str | dict[str, str]
    DATABASE_USERNAME: str | dict[str, str]
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    class Config:
        env_file = get_env_filename()
        env_file_encoding = "utf-8"

def get_environment_variables():
    returnValue = EnvironmentSettings()
    returnValue.DATABASE_HOSTNAME = json.loads(returnValue.DATABASE_HOSTNAME.replace("'", "\""))
    returnValue.DATABASE_NAME = json.loads(returnValue.DATABASE_NAME.replace("'", "\""))
    returnValue.DATABASE_PASSWORD = json.loads(returnValue.DATABASE_PASSWORD.replace("'", "\""))
    returnValue.DATABASE_PORT = json.loads(returnValue.DATABASE_PORT.replace("'", "\""))
    returnValue.DATABASE_USERNAME = json.loads(returnValue.DATABASE_USERNAME.replace("'", "\""))
    return returnValue