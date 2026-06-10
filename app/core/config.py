from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    admin_token: str = "happyhappyhappy"
    upstream_url: str = "https://brokenapi12345.com"
    db_url: str = "sqlite:///shadow.db"
    req_timeout: int = 10
    #use later
    cache_ttl: int = 3600

    class Config:
        env_file = ".env"

settings = Settings()