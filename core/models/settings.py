from __future__ import annotations
from pydantic import BaseSettings
from core.emuns import Mode


class Settings(BaseSettings):
    token: str
