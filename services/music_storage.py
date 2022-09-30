from pathlib import Path
import ffmpeg_downloader as ffdl
from discord import PCMVolumeTransformer, FFmpegPCMAudio


BASE_DIR = Path(__file__).resolve().parent.parent


class MusicStorage:

    def get(self, key: str):
        audio = FFmpegPCMAudio(BASE_DIR / f'{key}.mp3', executable=ffdl.ffmpeg_path)
        return PCMVolumeTransformer(audio, 0.5)