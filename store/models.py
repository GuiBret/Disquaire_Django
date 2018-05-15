from django.db import models

# Create your models here.
class Artist(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name

class Contact(models.Model):

    def __str__(self):
        return self.name

    email = models.EmailField(max_length=100)
    name = models.CharField(max_length=200)



class Album(models.Model):

    def __str__(self):
        return self.title

    reference = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add = True)
    available = models.BooleanField(default=True)
    title = models.CharField(max_length=200)
    picture = models.URLField()
    artists = models.ManyToManyField(Artist, related_name="albums", blank=True)


class Booking(models.Model):

    def __str__(self):
        return self.contact.name

    created_at = models.DateTimeField(auto_now_add = True)
    contacted = models.BooleanField(default=False)
    album = models.OneToOneField(Album, on_delete=models.CASCADE)
    contact = models.ForeignKey(Contact, on_delete = models.CASCADE)
