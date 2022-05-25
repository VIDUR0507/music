from django.shortcuts import render
from musicbeats2.models import Song, History, Listenlater
from django.db.models import Case, When
def index(request):
    song= Song.objects.all()[0:3]
    watch = []
    if request.user.username:
        wl= Listenlater.objects.filter(user=request.user)
        ids = []
        for i in wl:
            ids.append(i.video_id)

        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
        watch = Song.objects.filter(song_id__in=ids).order_by(preserved)    
        watch = reversed(watch)
    else:
        listen = Song.objects.all()[0:3]

    genreList = Song.objects.values('genre').distinct()
    ctx ={
        'songs':song,
        'laters': watch,
        'genreList': genreList,
    }
    return render(request,'index.html',ctx)


