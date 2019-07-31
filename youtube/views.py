from django.http import HttpResponse,HttpResponseRedirect
from django.template import loader
from youtube.yt_fetch import metadata, request_is_live, channel_feed, channel_info, channel_url, branding_settings, sitemap, latest_video_id
import os
from youtube.fb_scrape import fb_scrape

channel_domain = os.environ['channel_domain']




def index(request, video_id):
    meta = metadata(video_id)
    template = loader.get_template('youtube/index.html')
    context = {
        'live': str(request_is_live(request.path, video_id)),
        'channel_name' : meta['channel_name'],
        'video_id' : meta['video_id'],
        'og_title' : meta['og_title'],
        'og_image' : meta['og_image'],
        'og_description' : meta['og_description'],
        'twitter_title' : meta['twitter_title'],
        'twitter_description' : meta['twitter_description'],
        'twitter_image' : meta['twitter_image'],
        'channel_domain': channel_domain,
        'keywords': meta['keywords']
            }
    try:
        to_scrape = ''.join((request.scheme,'://',channel_domain,request.get_full_path(force_append_slash=False)))
        print("********")
        print("URL to scrape: ",to_scrape)
        print("********")
        fb_scrape(to_scrape)
    except:
        NameError("fb_access_token doen't appear to be defined")
    return HttpResponse(template.render(context,request))

def gift_guide(request, video_id="PzIghuJoC8I"):
    meta = metadata(video_id)
    template = loader.get_template('youtube/Holiday_Gift_Guide.html')
    context = {
        'live': str(request_is_live(request.path, video_id)),
        'channel_name' : meta['channel_name'],
        'video_id' : meta['video_id'],
        'og_title' : meta['og_title'],
        'og_image' : meta['og_image'],
        'og_description' : meta['og_description'],
        'twitter_title' : meta['twitter_title'],
        'twitter_description' : meta['twitter_description'],
        'twitter_image' : meta['twitter_image'],
        'channel_domain': channel_domain,
            }
    return HttpResponse(template.render(context,request))

def home(request, channel_id=os.environ['channel_id']):
    my_channel= branding_settings(channel_id)
    template = loader.get_template('youtube/home.html')
    context = {
        'url': channel_url(channel_id),
        'title':my_channel['title'],
        'description':my_channel['description'],
        'image':my_channel['image'],
        'domain':channel_domain
        }
    return HttpResponse(template.render(context,request))
    
    # return HttpResponseRedirect(channel_url(channel_id))

def subscribe(request, channel_id=os.environ['channel_id']):
    sub_link = ''.join([channel_url(channel_id),'/?sub_confirmation=1'])
    return HttpResponseRedirect(sub_link)

def redirect(request, url):
        return HttpResponseRedirect(url)

def feed(request, channel_id=os.environ['channel_id']):
    channel_feed_items = channel_feed(channel_id)
    channel_metadata = channel_info(channel_id)
    template = loader.get_template('youtube/feed.html')
    context = {
        'items': channel_feed_items['items'],
        'channel_name': channel_metadata['title'],
        'channel_description': channel_metadata['description'],
        'channel_thumbnail': channel_metadata['thumbnail_url'],
        'channel_id': channel_id,
        'channel_domain': channel_domain,
        'channel_url': channel_url(channel_id)

    }
    return HttpResponse(template.render(context,request))

def sitemap_render(request, channel_id=os.environ['channel_id']):
    sitemap_urls = sitemap(channel_id)
    template = loader.get_template('youtube/sitemap.xml')
    context = {
        'sitemapinfo':sitemap_urls
    }
    return HttpResponse(template.render(context,request))
    
    



def latest_video(request,channel_id=os.environ['channel_id']):
    video_id = latest_video_id(channel_id)
    return HttpResponseRedirect(''.join(["http://",os.environ['channel_domain'],"/",video_id]))

def latest_image(request,channel_id=os.environ['channel_id']):
    video_id = latest_video_id(channel_id)
    return HttpResponseRedirect(''.join(["http://", os.environ['channel_domain'], "/", video_id, '/image']))


def image_only(request, video_id):
   return HttpResponseRedirect(metadata(video_id)['og_image'])

def mobile_banner_image(request, channel_id=os.environ['channel_id']):
    return HttpResponseRedirect(branding_settings(channel_id)['mobile_banner'])