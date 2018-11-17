from django.urls import path

from . import views
import os
channel_id = os.environ['channel_id']

urlpatterns = [
    path('giftguide', views.gift_guide, name='giftguide'),
    path('', views.home, name='home'),
    path('clutterfree', views.redirect, {"url": "https://www.youtube.com/playlist?list=PLdr1YBmf_Da8dCv6FJ9cYWsrOxeqCVIrQ"}),
    path('clutter-free', views.redirect,{"url": "https://www.youtube.com/playlist?list=PLdr1YBmf_Da8dCv6FJ9cYWsrOxeqCVIrQ"}),
    path('android', views.redirect, {"url": "https://www.youtube.com/playlist?list=PLdr1YBmf_Da8do3vXAz72j8xGChHJM-3h"}),
    path('favicon.ico', views.redirect, {"url":"https://assets.geniuslounge.com/favicon.ico"}),
    path('static/favicon.ico', views.redirect, {"url":"https://assets.geniuslounge.com/favicon.ico"}),
    path('latest', views.latest_video),
    path('latest/image',views.latest_image),
    path('contribute', views.redirect, {"url":"http://www.youtube.com/timedtext_cs_panel?tab=2&c="+channel_id}),
    path('subscribe', views.subscribe),
    path('feed', views.feed, name='feed'),
    path('feed/<slug:channel_id>', views.feed, name='feed'),
    path('<slug:channel_id>/mobile_banner', views.mobile_banner_image, name='header_image'),
    path('mobile_banner', views.mobile_banner_image, name='header_image'),
    path('live/', views.home, name='live'),
    path('live', views.home, name='live'),
    path('live/<slug:video_id>', views.index, name='live'),
    path('<slug:video_id>/image', views.image_only),
    path('<slug:video_id>', views.index, name='index'),  # Needs to be last so all the other possibilites can go first.

]
