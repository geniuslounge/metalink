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
        return "https://geniuslounge.github.io/metalink/images/YouTubeLogo.png"

def request_is_live(request, video_id):
    """Determines is the request is coming from the /live endpoint. This affects the way the metadata is displayed for share links."""
    if request == "/live/"+video_id:
        return True
    else:
        return False


def channel_feed(channel_id, number_of_feed_items=25):
    """Outputs a RFC822 compatible RSS feed for the last 25 videos from a given channel_id"""
    payload = { 'part':'snippet',
                'channelId':channel_id,
                'maxResults':number_of_feed_items,
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
    
    # blog={
    #     "kind": "youtube#channelListResponse",
    #   "etag": "\"XI7nbFXulYBIpL0ayR_gDh3eu1k/Kxm_7m7IjfohqxvNQoTq92Fkj44\"",
    #   "pageInfo": {
    #     "totalResults": 1,
    #     "resultsPerPage": 1
    #   },
    #   "items": [
    #     {
    #       "kind": "youtube#channel",
    #       "etag": "\"XI7nbFXulYBIpL0ayR_gDh3eu1k/YWcLxiRhr1-6mJf-rxQnPDMTN14\"",
    #       "id": "UCU261fOCKtUwxigoCcZuVHQ",
    #       "brandingSettings": {
    #         "channel": {
    #           "title": "Genius Lounge",
    #           "description": "Free training for the tech in your life. \nWe provide free training for your iPhone, Android, and a bunch more! Maybe you're new to your device, or perhaps you want to learn those cool tricks to show your friends. Check us out to learn a little more about the tech you already own. Unleash your inner Genius and join us in the Genius Lounge.",
    #           "keywords": "\"Genius Lounge\" GeniusLounge tech training iOS Android Apple \"iPhone help\" \"iPhone for beginners\" \"iPad for Beginners\" \"Free tech training\"",
    #           "defaultTab": "Featured",
    #           "trackingAnalyticsAccountId": "UA-113382064-1",
    #           "moderateComments": True,
    #           "showRelatedChannels": True,
    #           "showBrowseView": True,
    #           "unsubscribedTrailer": "5VbI9ruv3co",
    #           "profileColor": "#000000",
    #           "country": "US"
    #         },
    #         "image": {
    #           "bannerImageUrl": "https://yt3.ggpht.com/O3MpsaRIBlZ452Ej7Q5mW_O1G5SZgExAuuJVRJ_N27uRpI6nNIEgFZNG9dcvKTSdMKRyBFh6LOU=w1060-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no",
    #           "bannerMobileImageUrl": "https://yt3.ggpht.com/O3MpsaRIBlZ452Ej7Q5mW_O1G5SZgExAuuJVRJ_N27uRpI6nNIEgFZNG9dcvKTSdMKRyBFh6LOU=w640-fcrop64=1,32b75a57cd48a5a8-nd-c0xffffffff-rj-k-no",
    #           "bannerTabletLowImageUrl": "https://yt3.ggpht.com/O3MpsaRIBlZ452Ej7Q5mW_O1G5SZgExAuuJVRJ_N27uRpI6nNIEgFZNG9dcvKTSdMKRyBFh6LOU=w1138-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no",
    #           "bannerTabletImageUrl": "https://yt3.ggpht.com/O3MpsaRIBlZ452Ej7Q5mW_O1G5SZgExAuuJVRJ_N27uRpI6nNIEgFZNG9dcvKTSdMKRyBFh6LOU=w1707-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no",
    #           "bannerTabletHdImageUrl": "https://yt3.ggpht.com/O3MpsaRIBlZ452Ej7Q5mW_O1G5SZgExAuuJVRJ_N27uRpI6nNIEgFZNG9dcvKTSdMKRyBFh6LOU=w2276-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no",
    #           "bannerTabletExtraHdImageUrl": "https://yt3.ggpht.com/O3MpsaRIBlZ452Ej7Q5mW_O1G5SZgExAuuJVRJ_N27uRpI6nNIEgFZNG9dcvKTSdMKRyBFh6LOU=w2560-fcrop64=1,00005a57ffffa5a8-nd-c0xffffffff-rj-k-no",
    #           "bannerMobileLowImageUrl": "https://yt3.ggpht.com/O3MpsaRIBlZ452Ej7Q5mW_O1G5SZgExAuuJVRJ_N27uRpI6nNIEgFZNG9dcvKTSdMKRyBFh6LOU=w320-fcrop64=1,32b75a57cd48a5a8-nd-c0xffffffff-rj-k-no",
    #           "bannerMobileMediumHdImageUrl": "https://yt3.ggpht.com/O3MpsaRIBlZ452Ej7Q5mW_O1G5SZgExAuuJVRJ_N27uRpI6nNIEgFZNG9dcvKTSdMKRyBFh6LOU=w960-fcrop64=1,32b75a57cd48a5a8-nd-c0xffffffff-rj-k-no",
    #           "bannerMobileHdImageUrl": "https://yt3.ggpht.com/O3MpsaRIBlZ452Ej7Q5mW_O1G5SZgExAuuJVRJ_N27uRpI6nNIEgFZNG9dcvKTSdMKRyBFh6LOU=w1280-fcrop64=1,32b75a57cd48a5a8-nd-c0xffffffff-rj-k-no",
    #           "bannerMobileExtraHdImageUrl": "https://yt3.ggpht.com/O3MpsaRIBlZ452Ej7Q5mW_O1G5SZgExAuuJVRJ_N27uRpI6nNIEgFZNG9dcvKTSdMKRyBFh6LOU=w1440-fcrop64=1,32b75a57cd48a5a8-nd-c0xffffffff-rj-k-no",
    #           # "bannerTvImageUrl": "https://yt3.ggpht.com/O3MpsaRIBlZ452Ej7Q5mW_O1G5SZgExAuuJVRJ_N27uRpI6nNIEgFZNG9dcvKTSdMKRyBFh6LOU=w2120-fcrop64=1,00000000ffffffff-nd-c0xffffffff-rj-k-no",
    #           # "bannerTvLowImageUrl": "https://yt3.ggpht.com/O3MpsaRIBlZ452Ej7Q5mW_O1G5SZgExAuuJVRJ_N27uRpI6nNIEgFZNG9dcvKTSdMKRyBFh6LOU=w854-fcrop64=1,00000000ffffffff-nd-c0xffffffff-rj-k-no",
    #           # "bannerTvMediumImageUrl": "https://yt3.ggpht.com/O3MpsaRIBlZ452Ej7Q5mW_O1G5SZgExAuuJVRJ_N27uRpI6nNIEgFZNG9dcvKTSdMKRyBFh6LOU=w1280-fcrop64=1,00000000ffffffff-nd-c0xffffffff-rj-k-no",
    #           # "bannerTvHighImageUrl": "https://yt3.ggpht.com/O3MpsaRIBlZ452Ej7Q5mW_O1G5SZgExAuuJVRJ_N27uRpI6nNIEgFZNG9dcvKTSdMKRyBFh6LOU=w1920-fcrop64=1,00000000ffffffff-nd-c0xffffffff-rj-k-no"
    #         },
    #         "hints": [
    #           {
    #             "property": "channel.featured_tab.template.string",
    #             "value": "Everything"
    #           },
    #           {
    #             "property": "channel.modules.show_comments.bool",
    #             "value": "True"
    #           },
    #           {
    #             "property": "channel.banner.mobile.medium.image.url",
    #             "value": "https://yt3.ggpht.com/O3MpsaRIBlZ452Ej7Q5mW_O1G5SZgExAuuJVRJ_N27uRpI6nNIEgFZNG9dcvKTSdMKRyBFh6LOU=w640-fcrop64=1,32b75a57cd48a5a8-nd-c0xffffffff-rj-k-no"
    #           }
    #         ]
    #       }
    #     }
    #   ]
    # }
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
