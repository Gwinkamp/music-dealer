from pydantic import BaseSettings, BaseModel


class SeafileSettings(BaseModel):
    username: str
    password: str
    base_url: str


class Settings(BaseSettings):
    token: str
    seafile: SeafileSettings
