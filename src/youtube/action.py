from typing import List, Dict
from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError

from logger import logger
from commons.utils import prettify_json

def _action_controller(YT: Resource, channel_id: str):
    is_resolved = False
    video_id_list = get_channel_videos(YT, channel_id)
    bot_comments = get_bot_comments(YT, video_id_list)
    if len(bot_comments) > 0:
        is_resolved = resolve_bot_comment(YT, bot_comments.pop(0))
    # if is_resolved and len(bot_comments) > 0:
    #     delete_bot_comments(YT, bot_comments)

    # logger.info(prettify_json(get_bot_comments(YT, video_id_list)))


def get_channel_videos(YT: Resource, channel_id: str) -> List[str]:
    """
    Fetches all videos in a given youtube channel.

    Args:
        YT (Resource): Authorized youtube resource object.
        channel_id (str): The id of the youtube channel.

    Returns:
        List[str]: A list of video ids in the given channel.
    """
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

    logger.info("Succeeded in fetching videos in channel")
    return videos

def get_bot_comments(YT: Resource, video_id_list: List[str]) -> List[Dict]:
    """
    Fetches comments from given videos that contain the bot name.

    Args:
        YT (Resource): Authorized youtube resource object.
        video_id_list (List[str]): A list of youtube video ids.

    Returns:
        List[str]: A list of comments that contain the bot name.
    """

    comments: List[Dict] = []
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

        # comments: List[Dict] = []
        while True:
            for item in response['items']:
                comment: str = item['snippet']['topLevelComment']['snippet']['textDisplay']

                if 'powerful' in comment.lower(): # TODO: change this to the bot name
                    comments.append(item)
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

    return comments

def resolve_bot_comment(YT: Resource, bot_comment: Dict) -> List[str]:
    bot_commands: List[str] = []
    comment: str = str(bot_comment['snippet']['topLevelComment']['snippet']['textDisplay'])
    bot_commands: List[str] = comment.split("\n")
    # logger.info(prettify_json(bot_comment))
    return bot_commands

def delete_bot_comments(YT: Resource, video_id_list: List[str]):
    """
    Delete bot comments from YouTube videos.

    This helps with cleaning up bot comments on YouTube videos.

    Args:
        YT (Resource): The YouTube API resource object.
        video_id_list (List[str]): A list of video IDs to delete comments from.
    """
    for video_id in video_id_list:
        request = YT.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            order="time"  # Newest comments first
        )

        try:
            response = request.execute()
        except HttpError as e:
            logger.error(f"Error fetching comments: {e}")
            continue

        while True:
            for item in response['items']:
                comment_id = item['snippet']['topLevelComment']['id']
                comment_text: str = item['snippet']['topLevelComment']['snippet']['textDisplay']

                if 'powerful' in comment_text.lower():  # TODO: Change this to your bot's keyword
                    try:
                        # Delete the comment
                        YT.comments().delete(id=comment_id).execute()
                        logger.info(f"Deleted comment with ID: {comment_id}")
                    except HttpError as e:
                        logger.error(f"Error deleting comment {comment_id}: {e}")

            if 'nextPageToken' in response:
                request = YT.commentThreads().list(
                    part="snippet",
                    videoId=video_id,
                    maxResults=100,
                    pageToken=response['nextPageToken'],
                    order="time"
                )
                try:
                    response = request.execute()
                except HttpError as e:
                    logger.error(f"Error fetching next page of comments: {e}")
                    break
            else:
                break
