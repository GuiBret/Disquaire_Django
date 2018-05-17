from django.http import HttpResponse
from django.shortcuts import render

from .models import Album, Artist, Contact, Booking




# Create your views here.
def index(request):

    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]

    return render(request, "store/index.html", {"albums": albums})

def albums(request):
    albums = Album.objects.filter(available=True)

    return render(request, "store/listing.html", {"albums": albums})

def detail(request, album_id):
    album = Album.objects.get(pk=album_id)
    artists = " ".join(artist.name for artist in album.artists.all())
    
    return render(request, "store/detail.html", {"album": album, "artists":artists})

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
