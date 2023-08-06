import logging
import src.database.connection as database
import src.database.utils as utils
from src.database.utils import DatabaseConfig
import src.api.okvendas as api_okvendas
from src.services import slack
from src.database import queries
import src

logger = logging.getLogger()

