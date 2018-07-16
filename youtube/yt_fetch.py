import json
import requests
from youtube.dates import format_to_RFC822
import os
yt_api_key = os.environ['yt_api_key']

def metadata(video_id):
    payload = {'id': video_id,
               'part': 'snippet,contentDetails,statistics',
               'key': yt_api_key
               }

    r = requests.get('https://www.googleapis.com/youtube/v3/videos', params=payload)
    statuscode = r.status_code
    blob = json.loads(r.text)

    return {'channel_name' : blob['items'][0]['snippet']['channelTitle'],
        'video_id': video_id,
        'og_title': blob['items'][0]['snippet']['title'],
        'og_image': get_best_image(blob),
        'og_description': blob['items'][0]['snippet']['description'],
        'twitter_title': blob['items'][0]['snippet']['title'],
        'twitter_description': blob['items'][0]['snippet']['description'],
        'twitter_image': get_best_image(blob)
            }


def request_is_live(request, video_id):
    if request == "/live/"+video_id:
        return True
    else:
        return False


def channel_feed(channel_id):
    payload = { 'part':'snippet',
                'channelId':channel_id,
                'maxResults':"25",
                'order':'date',
                'type':'video',
                'key':yt_api_key
    }

    r = requests.get('https://www.googleapis.com/youtube/v3/search', params=payload)
    blob = json.loads(r.text)

    for x in blob['items']:
        x['snippet']['pubDate'] = format_to_RFC822(x['snippet']['publishedAt'])
        x['snippet']['best_image'] = metadata(x['id']['videoId'])['og_image']

    return blob

def channel_info(channel_id):
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


def get_best_image(blob):
    if 'maxres' in blob['items'][0]['snippet']['thumbnails']:
        return blob['items'][0]['snippet']['thumbnails']['maxres']['url']
    elif 'standard' in blob['items'][0]['snippet']['thumbnails']:
        return blob['items'][0]['snippet']['thumbnails']['standard']['url']
    elif 'high' in blob['items'][0]['snippet']['thumbnails']:
        return blob['items'][0]['snippet']['thumbnails']['high']['url']
    elif 'medium' in blob['items'][0]['snippet']['thumbnails']:
        return blob['items'][0]['snippet']['thumbnails']['medium']['url']
    elif 'default' in blob['items'][0]['snippet']['thumbnails']:
        return blob['items'][0]['snippet']['thumbnails']['default']['url']
    else:
        return "http://assets.geniuslounge.com/YouTubeLogo.png"