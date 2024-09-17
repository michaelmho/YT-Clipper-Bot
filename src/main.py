from youtube.auth import get_youtube_service, channel_id
from youtube.action import get_channel_videos
from logger import logger

def main():
    logger.info("Starting the application")
    youtube_videos = get_channel_videos(get_youtube_service(), channel_id=channel_id)

    if youtube_videos is not None:
        logger.info('Succeeded in starting up')
        # TODO: Continue HERE <-e


if __name__ == "__main__":
    main()
