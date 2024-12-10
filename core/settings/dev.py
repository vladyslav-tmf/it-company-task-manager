from core.settings.base import *

SECRET_KEY = "a17^@^r@7v1e%4pqs(5n-$%curd+^_pxj+u$c8-^vx9q_8v-g)"
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
INTERNAL_IPS = ["localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}
