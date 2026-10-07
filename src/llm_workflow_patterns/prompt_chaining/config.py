import logging

from openai import OpenAI
from pydantic_settings import BaseSettings, SettingsConfigDict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    openai_api_key: str


settings = Settings()  # type: ignore
client = OpenAI(api_key=settings.openai_api_key)
MODEL = "gpt-4o"
