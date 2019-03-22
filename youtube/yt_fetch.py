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
    try:
        keyword_string = ', '.join(item['snippet']['tags'])
    except:
        keyword_string = ''

    return {'channel_name' : item['snippet']['channelTitle'],
        'video_id': video_id,
        'og_title': item['snippet']['title'],
        'og_image': get_best_image(item),
        'og_description': item['snippet']['description'],
        'twitter_title': item['snippet']['title'],
        'twitter_description': item['snippet']['description'],
        'twitter_image': get_best_image(item),
        'keywords': keyword_string
            }

def multi_metadata(video_id_list):
    """Gets YouTube metadata for a list of YouTube videos"""
    
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
        return "https://geniuslounge.github.io/metalink/images/YouTubeLogo.png"

def request_is_live(request, video_id):
    """Determines is the request is coming from the /live endpoint. This affects the way the metadata is displayed for share links."""
    if request == "/live/"+video_id:
        return True
    else:
        return False


def get_upload_playlist_for_channel(channel_id=os.environ['channel_id']):
    """Gets the upload playlist for the given channel"""
    url = "https://www.googleapis.com/youtube/v3/channels"
    
    querystring = {"key": yt_api_key,
                   "part": "contentDetails",
                   "id": channel_id}
    
    
    response = requests.request("GET", url, params=querystring)
    results = json.loads(response.text)
    playlist = results["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]
    return playlist

def latest_video_id(channel_id=os.environ['channel_id']):
    """Gets the latest video given the channel_id"""
    url = "https://www.googleapis.com/youtube/v3/playlistItems"

    querystring = {"key": yt_api_key, "part": "snippet,contentDetails",
                   "playlistId": get_upload_playlist_for_channel(channel_id),
                   "maxResults": "1"}

    response = requests.request("GET", url, params=querystring)
    
    results = json.loads(response.text)
    vidId = results['items'][0]['contentDetails']['videoId']
    return vidId
    
    


def channel_feed(channel_id, number_of_feed_items=25):
    """Outputs a RFC822 compatible RSS feed for the last 25 videos from a given channel_id"""
    payload = { 'part':'snippet',
                'playlistId':get_upload_playlist_for_channel(channel_id),
                'maxResults':number_of_feed_items,
                'key':yt_api_key
    }

    r = requests.get('https://www.googleapis.com/youtube/v3/playlistItems', params=payload)
    results_of_search = json.loads(r.text)
    video_list = []
    for video in results_of_search['items']:
        video_list.append(video['snippet']['resourceId']['videoId'])
    
    image_dict = get_multiple_best_images(multi_metadata(video_list))

    for x in results_of_search['items']:
        #These lines add keys to the dictionary that get parsed later
        x['snippet']['pubDate'] = format_to_RFC822(x['snippet']['publishedAt'])
        vid_id = x['snippet']['resourceId']['videoId']
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
    return_dict = {
        'title':blob['items'][0]['snippet']['title'],
        'description':blob['items'][0]['snippet']['description'],
        'thumbnail_url':blob['items'][0]['snippet']['thumbnails']['high']['url'],
        'channel_id':channel_id
    }
    if 'customUrl' in blob['items'][0]['snippet']:
        return_dict['customUrl']=blob['items'][0]['snippet']['customUrl']
    return return_dict


def channel_url(channel_id):
    channel_metadata = channel_info(channel_id)
    if 'customUrl' in channel_metadata:
        return ''.join(["https://www.youtube.com/c/",channel_metadata['customUrl']])
    else:
        return ''.join(["https://www.youtube.com/channel/",channel_metadata['channel_id']])



def branding_settings(channel_id=os.environ['channel_id']):
    payload = {
        'part':'brandingSettings',
        'id':channel_id,
        'key':yt_api_key
    }
    r = requests.get('https://www.googleapis.com/youtube/v3/channels', params=payload)
    
    blob = json.loads(r.text)
    
    channel_branding_settings = blob['items'][0]['brandingSettings']
    if 'bannerTvImageUrl' in channel_branding_settings['image']:
        bestimage = channel_branding_settings['image']['bannerTvImageUrl']
    elif 'bannerTvHighImageUrl' in channel_branding_settings['image']:
        bestimage = channel_branding_settings['image']['bannerTvHighImageUrl']
    elif 'bannerTvMediumImageUrl' in channel_branding_settings['image']:
        bestimage = channel_branding_settings['image']['bannerTvMediumImageUrl']
    elif 'bannerTvLowImageUrl' in channel_branding_settings['image']:
        bestimage = channel_branding_settings['image']['bannerTvLowImageUrl']
    else:
        bestimage='https://geniuslounge.github.io/metalink/images/YouTubeLogo.png'

    if 'bannerMobileExtraHdImageUrl' in channel_branding_settings['image']:
        mobile_banner = channel_branding_settings['image']['bannerMobileExtraHdImageUrl']
    elif 'bannerMobileHdImageUrl' in channel_branding_settings['image']:
        mobile_banner = channel_branding_settings['image']['bannerMobileHdImageUrl']
    elif 'bannerMobileMediumHdImageUrl' in channel_branding_settings['image']:
        mobile_banner = channel_branding_settings['image']['bannerMobileMediumHdImageUrl']
    elif 'bannerMobileLowImageUrl' in channel_branding_settings['image']:
        mobile_banner = channel_branding_settings['image']['bannerMobileLowImageUrl']
    else:
        mobile_banner='https://geniuslounge.github.io/metalink/images/YouTubeLogo.png'
    
        
    
    return_dict = {
        'url':channel_url(channel_id),
        'image':bestimage,
        'mobile_banner':mobile_banner,
        'title':channel_branding_settings['channel']['title'],
        'description':channel_branding_settings['channel']['description']
    }
    return return_dict

def sitemap(channel_id=os.environ['channel_id']):
    payload = {
        'part': 'snippet',
        'id': channel_id,
        'key': yt_api_key,
        'maxResults': '50',
        'order':'date',
        'channelId': channel_id,
        'type':'video'
    }
    r = requests.get('https://www.googleapis.com/youtube/v3/search', params=payload)
    
    blob = json.loads(r.text)
    sitemap_info = []
    for x in blob['items']:
        sitemap_info.append(''.join(['http://www.', os.environ['channel_domain'],'/',x['id']['videoId']]))
    return sitemap_info

if __name__ == '__main__':
    get_upload_playlist_for_channel("UCU261fOCKtUwxigoCcZuVHQ")