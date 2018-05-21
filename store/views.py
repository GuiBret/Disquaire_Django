from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from .models import Album, Artist, Contact, Booking

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


# Create your views here.
def index(request): # Displays latest albums

    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
    context = {
        "albums": albums,
        "page_title": "Nos derniers albums"
   }

    return render(request, "store/index.html", context)

def albums(request): # Displays all albums

    album_list = Album.objects.filter(available=True)

    page = request.GET.get('page')

    paginator = Paginator(album_list, 3)

    try:
        albums = paginator.page(page)
    except PageNotAnInteger:
        albums = paginator.page(1)
    except EmptyPage:
        albums = paginator.page(paginator.num_pages)

    context = {
        "albums": albums,
        "page_title": "Tous nos albums",
        "paginate": True
        }

    return render(request, "store/listing.html", context)

def detail(request, album_id):

    album = get_object_or_404(Album, pk=album_id)
    artists = " ".join(artist.name for artist in album.artists.all())

    context = {
        "album": album,
        "artists":artists
    }
    return render(request, "store/detail.html", context)

def search(request):
    query = request.GET.get('query')
    message = ""

    if not query:
        albums = Album.objects.all()
    else:
        albums = Album.objects.filter(title__icontains=query)

        if not albums.exists():
            albums = Album.objects.filter(artists__name__icontains=query)

    context = {
        "query": query,
        "albums": albums
    }

    return render(request, "store/search.html", context)
