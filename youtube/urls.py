from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('clutterfree', views.redirect, {"url": "https://www.youtube.com/playlist?list=PLdr1YBmf_Da8dCv6FJ9cYWsrOxeqCVIrQ"}),
    path('clutter-free', views.redirect,{"url": "https://www.youtube.com/playlist?list=PLdr1YBmf_Da8dCv6FJ9cYWsrOxeqCVIrQ"}),
    path('android', views.redirect, {"url": "https://www.youtube.com/playlist?list=PLdr1YBmf_Da8do3vXAz72j8xGChHJM-3h"}),
    path('favicon.ico', views.redirect, {"url":"https://assets.geniuslounge.com/favicon.ico"}),
    path('static/favicon.ico', views.redirect, {"url":"https://assets.geniuslounge.com/favicon.ico"}),
    path('latest', views.redirect, {"url":"https://www.tubebuddy.com/quicknav/latest/UCU261fOCKtUwxigoCcZuVHQ"}),
    path('feed/<slug:channel_id>', views.feed, name='feed'),
    path('live/', views.home, name='live'),
    path('live', views.home, name='live'),
    path('live/<slug:video_id>', views.index, name='live'),
    path('<slug:video_id>', views.index, name='index'), # Needs to be last so all the other possibilites can go first.
]