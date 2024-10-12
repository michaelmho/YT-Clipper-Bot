from youtube.auth import get_youtube_service, channel_id
from youtube.action import _youtube_controller
from logger import logger

def main():
    logger.info("Starting the application")

    _youtube_controller(get_youtube_service(), channel_id=channel_id)

    logger.info("Application finished")


if __name__ == "__main__":
    main()
