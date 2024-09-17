from dotenv import load_dotenv
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from logger import logger
import os

load_dotenv()

api_key = os.getenv('YOUTUBE_V3_API_KEY')
channel_id = os.getenv('CHANNEL_ID')


def get_youtube_service() -> Resource:
    """
    Instantiates the Youtube service resource, contains and makes use of the api_key & channel_id
    """
    try:
        youtube: Resource = build('youtube', 'v3', developerKey=api_key, cache_discovery=False)
        logger.info("Youtube API service initialized successfully!")
        return youtube
    except HttpError as e:
        logger.error(f"An error occurred while instantiating the youtube resource build: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
