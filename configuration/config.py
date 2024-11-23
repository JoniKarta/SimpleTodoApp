from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=r"C:\Users\jkart\PycharmProjects\TodoApp\SimpleTodoApp\.env",
    )

    DATABASE_URL: str
    JWT_SECRET_KEY: str
    DEV_ENVIRONMENT: bool
    ROOT_PREFIX_VERSION: str = "v1"
