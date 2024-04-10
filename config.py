from environs import Env

env = Env()
env.read_env()

DB_URI = env.str("DB_URI")
TESTING = env.bool("TESTING", False)
if TESTING:
    DB_URI = env.str("TEST_DB_URI")
JWT_SECRET_KEY = env.str("JWT_SECRET_KEY", "secret-key")

BIZFLY_API_KEY = env.str("BIZFLY_API_KEY", "bizfly-api-key")
