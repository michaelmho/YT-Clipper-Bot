import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),  # Log to a file
        logging.StreamHandler()          # Log to console
    ]
)

logger = logging.getLogger(__name__)
# logging.getLogger('googleapiclient.discovery').setLevel(logging.INFO)
# TODO: Change logging level to INFO
