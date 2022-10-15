class FFmpegNotFound(RuntimeError):

    def __str__(self):
        return 'Не установлен ffmpeg! Для работы бота необходима утилита ffmpeg'
