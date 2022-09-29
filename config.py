
from core.models import Settings
from core.emuns import Mode

mode = Mode.from_env()
settings = Settings(_env_file='.env')
