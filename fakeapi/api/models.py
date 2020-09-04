from django.db import models
from django.contrib.auth.models import User


def image_path(instance, filename):
    return '{}/photos/{}'.format(instance.userprofile.user.username, filename)
    
def profile_picture_path(instance, filename):
    return '{}/{}'.format(instance.user.username, filename)

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=100, blank=False, null=False)
    profile_picture = models.ImageField(upload_to=profile_picture_path, blank=False, null=False)

class Photo(models.Model):
    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=False, blank=False)
    image = models.ImageField(upload_to=image_path, blank=False, null=False)