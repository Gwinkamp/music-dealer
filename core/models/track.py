from pydantic import BaseModel
from discord import AudioSource


class Track(BaseModel):
    name: str
    is_playing: bool
    source: AudioSource

    class Config:
        arbitrary_types_allowed = True
