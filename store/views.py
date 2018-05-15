from django.http import HttpResponse
from store.models import Album, Artist
#from .models import ALBUMS

# Create your views here.
def index(request):
    message = "Salut tout le monde !"
    albums = Album.objects.filter(available=True).order_by('-created_at')[:12]

    formatted_albums = ["<li>{}</li>".format(album.title) for album in albums]
    message = """<ul>{}</ul>""".format("\n".join(formatted_albums))
    return HttpResponse(message)

def albums(request):
    albums = Album.objects.filter(available=True)
    list_albums = ["<li>{}</li>".format(album.title) for album in albums]

    message = """<ul>{}</ul>""".format("\n".join(list_albums))
    return HttpResponse(message)

def detail(request, album_id):
    id = int(album_id)
    album = ALBUMS[id]

    artists = " ".join([artist['name'] for artist in album["artists"]])

    message = "Le nom de l'album est {}. Il a été écrit par {}.".format(album['name'], artists)

    return HttpResponse(message)

def search(request):
    obj = str(request.GET)
    query = request.GET.get("query")

    if not query:
        message = "Aucun artiste n'est demandé"
    else:
        albums = [
            album for album in ALBUMS
            if query in " ".join(artist['name'] for artist in album['artists'])
        ]

        if len(albums) == 0:
            message = "Misère de misère, nous n'avons trouvé aucun résultat ! "
        else:
            albums = ["<li>{}</li>".format(album['name']) for album in albums]
            message = """
                Nous avons trouvé les albums correspondant à votre requête ! Les voici :
                <ul>
                    {}
                </ul>
            """.format("</li><li>".join(albums))

    return HttpResponse(message)
