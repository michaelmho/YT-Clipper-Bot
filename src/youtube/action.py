from typing import List
from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError

from logger import logger
from commons.utils import prettify_json

def get_channel_videos(YT: Resource, channel_id: str):
    videos = []
    next_page_token = None

    logger.info("Attempting to fetch videos in channel")
    while True:
        try:
            request = YT.search().list(
                part='snippet',
                channelId=channel_id,
                maxResults=50,
                pageToken=next_page_token,
                type='video'
            )
            response = request.execute()
        except Exception as e:
            logger.error(f"An error occurred while getting all youtube videos of the channel: {e}")

        for item in response['items']:
            video_data = {
                'title': item['snippet']['title'],
                'videoId': item['id']['videoId'],
                'publishedAt': item['snippet']['publishedAt']
            }
            videos.append(video_data['videoId'])

        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break

    logger.info(prettify_json(get_bot_comments(YT, videos)))


def get_bot_comments(YT: Resource, video_id_list: List[str]):
    bot_comments = []
    for video_id in video_id_list:
        request = YT.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            order="time"
        )

        try:
            logger.info("Attempting to get bot comments")
            response = request.execute()
        except HttpError as e:
            logger.error(f"Error fetching comments: {e}")

        while True:
            for item in response['items']:
                comment: str = item['snippet']['topLevelComment']['snippet']['textDisplay']

                if 'powerful' in comment.lower(): # TODO: change this to the bot name
                    bot_comments.append(comment)
                    # TODO: Figure out scheduling for bot to handle 1 comment at a time

            # Paginate
            if 'nextPageToken' in response:
                request = YT.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=100,
                    order="time",
                    pageToken=response['nextPageToken']
                )
                try:
                    response = response.execute()
                except HttpError as e:
                    logger.error(f"Error fetching comments: {e}")
                    break
            else:
                break

    return bot_comments

