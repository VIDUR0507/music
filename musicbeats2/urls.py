from django.urls import path
from.import views
from django.conf.urls.static import static

urlpatterns = [
    path('songs/',views.songs,name='songs'),
    path('songs/<int:id>',views.songpost,name='songspost'),
    path('login',views.login,name='login'),
    path('signup',views.signup,name='signup'),
    path('logout_user',views.logout_user,name='logout_user'),
    path('listenlater',views.listenlater,name='listenlater'),
    path('player', views.player, name='player'),
    path('player/media/<int:id>', views.play_song, name='single_song'),
    path('history',views.history, name='history'),
    path('c/<str:channel>',views.channel, name='channel'),
    path('upload',views.upload, name='upload'),
    path('search',views.search, name='search'),
    path('genre/<str:genre>',views.genre_view, name='genre'),
] 
