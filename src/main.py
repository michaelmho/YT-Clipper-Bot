from youtube.auth import get_youtube_service, channel_id
from youtube.action import _action_controller
from logger import logger

def main():
    logger.info("Starting the application")

    _action_controller(get_youtube_service(), channel_id=channel_id)

    logger.info("Application finished")


if __name__ == "__main__":
    main()
