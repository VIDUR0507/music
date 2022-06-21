from multiprocessing import AuthenticationError
from unicodedata import name
from django.shortcuts import render
from musicbeats2.models import Song, Listenlater, History, Channel
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Case, When

def index(request):
    song= Song.objects.all()[0:8]

    if request.user.is_authenticted:
        wl= Listenlater.objects.filter(user=request.user)
        ids = []
        for i in wl:
            ids.append(i.video_id)

        preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
        watch = Song.objects.filter(song_id__in=ids).order_by(preserved)
        watch = reversed(watch)
    else:
        listen = Song.objects.all()[0:8]

    return render(request,'index.html',{'song':song, 'watch': watch})

def history(request):
    if request.method=="POST":
        user = request.user
        music_id = request.POST['music_id']
        history = History(user=user, music_id=music_id)
        history.save()

        return redirect(f"/musicbeats2/songs/{music_id}")

    history=History.objects.filter(user=request.user)
    ids = []
    for i in history:
        ids.append(i.music_id)
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song=Song.objects.filter(song_id__in=ids).order_by(preserved)

    return render(request,'musicbeats2/history.html',{"history":song})

def listenlater(request):
    if request.method=="POST":
        user = request.user
        video_id= request.POST['video_id']
        listen = Listenlater.objects.filter(user=user)
        for i in listen:
            if video_id==i.video_id:
                message="Your song is already added"
                break
        else:
            listenlater= Listenlater(user=user, video_id=video_id,)
            listenlater.save()
            message ="Your Song is Successfully added"
        song=Song.objects.filter(song_id=video_id).first()
        return render(request,f"musicbeats2/songpost.html", {'song':song,"message":message})
    wl=Listenlater.objects.filter(user=request.user)
    ids = []
    for i in wl:
        ids.append(i.video_id)
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(ids)])
    song=Song.objects.filter(song_id__in=ids).order_by(preserved)

    return render(request,"musicbeats2/listenlater.html",{'song': song})

def songs(request):
    song=Song.objects.all()
    return render(request, 'musicbeats2/songs.html',{'song':song})

def songpost(request, id):
    song=Song.objects.filter(song_id=id).first()
    return render(request, 'musicbeats2/songpost.html',{'song':song})


def login(request):

    if request.method=="POST":
        userName=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=userName, password=password)
        from django.contrib.auth import login
        login(request, user)
        #if userName and password:
           # messages.success(request, 'Your message has been sent successfully.')
        #elif not userName:
           # messages.error(request, 'Please enter your name.')
        #elif not password:
            #essages.error(request, 'Please enter your password.')
        return redirect('/')

    return render(request, 'musicbeats2/login.html')
    

def signup(request):
    if request.method=="POST":
        email=request.POST['email']
        username=request.POST['username']
        first_name=request.POST['firstname']
        last_name=request.POST['lastname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        
        myuser=User.objects.create_user(username,email, pass1)
        myuser.first_name=first_name
        myuser.last_name=last_name
       
        myuser.save()
        user=authenticate(username=username, password=pass1)
        from django.contrib.auth import login
        login(request, user)

        channel=Channel(name=username)
        channel.save()
        return redirect('/')

    return render(request, 'musicbeats2/signup.html')

def logout_user(request):
    logout(request)
    return redirect("/")

def player(request):
    listenLaters = Listenlater.objects.filter(user=request.user).all()
    songs = Song.objects.filter(song_id__in=[listenLater.video_id for listenLater in listenLaters]).all()
    print(songs)
    paginator= Paginator(songs,1)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context={"page_obj":page_obj}
    return render(request,'musicbeats2/player.html',context)

def play_song(request,id):
    song=Song.objects.filter(song_id=id).first()
    context={"item":song}
    return render(request,'musicbeats2/single_player.html',context)

def channel(request, channel):
    chan = Channel.objects.filter(name=channel).first()
    video_ids = str(chan.music).split(" ")[1:]
    
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(video_ids)])
    song=Song.objects.filter(song_id__in=video_ids).order_by(preserved)

    return render(request,"musicbeats2/channel.html",{"channel":chan, "song":song})

def upload(request):
    if request.method=="POST":
        name=request.POST['name']
        singer=request.POST['singer']
        genre=request.POST['genre']
        movie=request.POST['movie']
        image=request.FILES['image']
        song1=request.FILES['file']
        if name and singer and genre and movie and image and song1:
            messages.success(request, 'Your Song has been uploaded successfully.')
        elif not name:
            messages.error(request, 'Please enter your name.')
        elif not singer:
            messages.error(request, 'Please enter your singer.')
        elif not genre:
            messages.error(request, 'Please enter your genre.')
        elif not movie:
            messages.error(request, 'Please enter your movie.')
        #elif not image:
            #messages.error(request, 'Please enter your image.')
        #elif not song1:
            #messages.error(request, 'Please enter your song.')

        song_model=Song(name=name, singer=singer, genre=genre, image=image, movie=movie, song=song1)
        song_model.save()

        music_id = song_model.song_id
        channel_find = Channel.objects.filter(name=str(request.user))
        print(channel_find)

        for i in channel_find:
            i.music += f" {music_id}"
            i.save()

    return render(request,"musicbeats2/upload.html")

def search(request):
    query = request.GET.get("query")
    song = Song.objects.all()
    channel_q = Channel.objects.all().filter(name__icontains=query)
    qs = song.filter(name__icontains=query)

    return render(request, "musicbeats2/search.html",{"song": qs, "query":query,})


def genre_view(request,genre):
    songs = Song.objects.filter(genre=genre).all()
    return render(request, "musicbeats2/genre.html", {"songs":songs})