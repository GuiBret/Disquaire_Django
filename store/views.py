from django.http import HttpResponse
from django.shortcuts import render

from .models import Album, Artist, Contact, Booking




# Create your views here.
def index(request): # Displays latest albums

    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]
    context = {
        "albums": albums,
        "page_title": "Nos derniers albums"
   }

    return render(request, "store/index.html", context)

def albums(request): # Displays all albums
    albums = Album.objects.filter(available=True)

    context = {
        "albums": albums,
        "page_title": "Tous nos albums"
        }

    return render(request, "store/listing.html", context)

def detail(request, album_id):
    album = Album.objects.get(pk=album_id)
    artists = " ".join(artist.name for artist in album.artists.all())

    context = {
        "album": album,
        "artists":artists
    }
    return render(request, "store/detail.html", context)

def search(request):
    query = request.GET.get('query')
    if not query:
        albums = Album.objects.all()
    else:
        albums = Album.objects.filter(title__icontains=query)

        if not albums.exists():
            albums = Album.objects.filter(artists__name__icontains=query)

        if not albums.exists():
            message = "Misère de misère, nous n'avons trouvé aucun résultat ! "


        else:
            albums = ["<li>{}</li>".format(album.title) for album in albums]
            message = """
                Nous avons trouvé les albums correspondant à votre requête ! Les voici :
                <ul>
                    {}
                </ul>
            """.format("</li><li>".join(albums))

    return HttpResponse(message)
