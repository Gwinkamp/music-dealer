from typing import Any, Coroutine, Callable
from discord import AudioSource
from .track import Track


class DelayedTrack(Track):
    source_filling_func: Callable[[], Coroutine[Any, Any, AudioSource]]
