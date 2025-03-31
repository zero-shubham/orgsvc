from dotenv import load_dotenv
from os import getenv

load_dotenv()

# Database connection settings
DATABASE_URL = getenv(
    "DATABASE_URL", "postgresql://user:password@localhost/dbname")
