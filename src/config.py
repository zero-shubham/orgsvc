from dotenv import load_dotenv
from os import getenv

load_dotenv()

# Database connection settings
DATABASE_URL = getenv(
    "DATABASE_URL", "postgresql://user:password@localhost/dbname")

SERVICE_NAME = getenv(
    "SERVICE_NAME", "orgsvc"
)
OLTP_HTTP_TRACE_ENDPOINT = getenv(
    "OLTP_HTTP_TRACE_ENDPOINT"
)
OLTP_HTTP_METER_ENDPOINT = getenv(
    "OLTP_HTTP_METER_ENDPOINT"
)
