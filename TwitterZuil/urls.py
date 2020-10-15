from django.urls import path
from TwitterZuil import views
urlpatterns = [
    path('', views.index, name='index'),
    path('Tweet', views.tweet_page, name='tweet_page'),
    path('SendTweet', views.send_tweet, name='send_tweet'),
    path('Review-Tweet', views.review_tweet, name='review_tweet'),
    path('Aanmelden-Moderator', views.aanmelden_moderator, name='aanmelden_moderator'),
    path('Handle-Review', views.handle_review_tweet, name='handle_review_tweet'),
    path('Scherm-Aanmaken', views.scherm_aanmaken, name='scherm-aanmaken'),
    path('Scherm-Toevoegen', views.scherm_toevoegen, name='scherm-toevoegen'),
    path('Scherm-Weergeven', views.scherm_kiezen, name='scherm_weergeven'),
    path('Scherm-Verversen/<id>', views.scherm_verversen, name='scherm_verversen'),
    path('Scherm/<id>', views.scherm_weergeven, name='scherm_activeren'),
    path('Aanmaken-Moderator', views.moderator_aanmaken, name='moderator_aanmaken'),
    path('Toevoegen-Moderator', views.moderator_toevoegen, name='moderator_toevoegen'),
]