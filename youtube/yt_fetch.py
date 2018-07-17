import json
import requests
from youtube.dates import format_to_RFC822
import os
yt_api_key = os.environ['yt_api_key']

def metadata(video_id):
    """Gets YouTube metadata for a single YouTube video"""
    payload = {'id': video_id,
               'part': 'snippet,contentDetails,statistics',
               'key': yt_api_key
               }

    r = requests.get('https://www.googleapis.com/youtube/v3/videos', params=payload)
    blob = json.loads(r.text)
    item = blob['items'][0]

    return {'channel_name' : item['snippet']['channelTitle'],
        'video_id': video_id,
        'og_title': item['snippet']['title'],
        'og_image': get_best_image(item),
        'og_description': item['snippet']['description'],
        'twitter_title': item['snippet']['title'],
        'twitter_description': item['snippet']['description'],
        'twitter_image': get_best_image(item)
            }

def multi_metadata(video_id_list):
    """Gets YouTube metadata for a single YouTube video"""
    
    video_id_list = ",".join(video_id_list)
    payload = {'id': video_id_list,
               'part': 'snippet,contentDetails,statistics',
               'key': yt_api_key
               }

    r = requests.get('https://www.googleapis.com/youtube/v3/videos', params=payload)
    results = json.loads(r.text)
    return results
    
def get_multiple_best_images(results_from_multi_metadata):
    """Gets the best image for multiple YouTube videos from the dictionary passed from multi_metadata()"""
    image_list={}
    for x in results_from_multi_metadata['items']:
        id = x['id']
        image_list[id] = get_best_image(x)
    return image_list


def get_best_image(item):
    """Determines the best image for a given video metadata blob """
    if 'maxres' in item['snippet']['thumbnails']:
        return item['snippet']['thumbnails']['maxres']['url']
    elif 'standard' in item['snippet']['thumbnails']:
        return item['snippet']['thumbnails']['standard']['url']
    elif 'high' in item['snippet']['thumbnails']:
        return item['snippet']['thumbnails']['high']['url']
    elif 'medium' in item['snippet']['thumbnails']:
        return item['snippet']['thumbnails']['medium']['url']
    elif 'default' in item['snippet']['thumbnails']:
        return item['snippet']['thumbnails']['default']['url']
    else:
        return "https://geniuslounge.github.io/share2/images/YouTubeLogo.png"

def request_is_live(request, video_id):
    """Determines is the request is coming from the /live endpoint. This affects the way the metadata is displayed for share links."""
    if request == "/live/"+video_id:
        return True
    else:
        return False


def channel_feed(channel_id):
    """Outputs a RFC822 compatible RSS feed for the last 25 videos from a given channel_id"""
    payload = { 'part':'snippet',
                'channelId':channel_id,
                'maxResults':"25",
                'order':'date',
                'type':'video',
                'key':yt_api_key
    }

    r = requests.get('https://www.googleapis.com/youtube/v3/search', params=payload)
    results_of_search = json.loads(r.text)
    video_list = []
    for video in results_of_search['items']:
        video_list.append(video['id']['videoId'])
    
    image_dict = get_multiple_best_images(multi_metadata(video_list))
    

    for x in results_of_search['items']:
        x['snippet']['pubDate'] = format_to_RFC822(x['snippet']['publishedAt'])
        vid_id = x['id']['videoId']
        x['snippet']['best_image'] = image_dict[vid_id]

    return results_of_search

def channel_info(channel_id):
    """Gets the channel metadata for a given channel"""
    payload = {
        'part':'snippet',
        'id': channel_id,
        'key': yt_api_key
    }

    r = requests.get('https://www.googleapis.com/youtube/v3/channels', params=payload)

    blob = json.loads(r.text)

    return {
        'title':blob['items'][0]['snippet']['title'],
        'description':blob['items'][0]['snippet']['description'],
        'thumbnail_url':blob['items'][0]['snippet']['thumbnails']['high']['url']

    }
