import logging
import pytz
from datetime import datetime
import os

timezone = pytz.timezone(os.environ.get("TIMEZONE", "UTC"))


class DateFormatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        dt = datetime.fromtimestamp(record.created, timezone)
        if datefmt:
            return dt.strftime(datefmt)
        return dt.isoformat()


# Configure Logging
formatter = DateFormatter(fmt="%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

handler = logging.StreamHandler()
handler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(handler)
