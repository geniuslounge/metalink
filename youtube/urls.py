from django.urls import path

from . import views
import os
channel_id = os.environ['channel_id']

urlpatterns = [
    path('', views.home, name='home'),
    path('favicon.ico', views.redirect, {"url":"https://assets.geniuslounge.com/favicon.ico"}),
    path('static/favicon.ico', views.redirect, {"url":"https://assets.geniuslounge.com/favicon.ico"}),
    path('latest', views.latest_video),
    path('latest/image',views.latest_image),
    path('subscribe', views.subscribe),
    path('feed', views.feed, name='feed'),
    path('sitemap.xml',views.sitemap_render, name='sitemap'),
    path('mobile_banner', views.mobile_banner_image, name='header_image'),
    path('channel/<slug:channel_id>', views.home, name='home'),
    path('channel/<slug:channel_id>/latest', views.latest_video),
    path('channel/<slug:channel_id>/latest/image', views.latest_image),
    path('channel/<slug:channel_id>/feed', views.feed, name='feed'),
    path('channel/<slug:channel_id>/mobile_banner', views.mobile_banner_image, name='header_image'),
    path('<slug:video_id>/image', views.image_only),
    path('<slug:video_id>', views.index, name='index'),  # Needs to be last so all the other possibilities can go first.

]


# Adding this so that any forks don't have to host the gift guide
if os.environ['channel_id'] == "UCU261fOCKtUwxigoCcZuVHQ":
    urlpatterns.insert(0,path('giftguide', views.gift_guide, name='giftguide'))