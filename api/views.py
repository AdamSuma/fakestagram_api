from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action 
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from .models import UserProfile, Photo
from .serializers import *

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (TokenAuthentication, )


    @action(detail=False, methods=['POST'])
    def register(self, request):
        try:
            user = User(username=request.data['username'], password=request.data['password'])
            userprofile = UserProfile(user=user, bio=request.data['bio'], profile_picture=request.data['profile_picture'])
            user.save()
            userprofile.save()
            token = Token.objects.create(user=user)
            return Response({"message": "Registered Successfully", "token": str(token) })
        except:
            return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['POST'])
    def edit(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "You must be logged in"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            request.user.userprofile.bio = request.data['bio']
            request.user.userprofile.profile_picture = request.data['profile_picture']
            request.user.save()
            return Response({"message": "Edited Successfully"})
        except:
            return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

class PhotoViewSet(viewsets.ModelViewSet):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    authentication_classes = (TokenAuthentication, )

    @action(detail=False, methods=["POST", "GET"])
    def request_photos(self, request):
        print(request.data)
        if not request.user.is_authenticated:
            print(request.user.username)
            return Response({"error": "You must be logged in"}, status=status.HTTP_401_UNAUTHORIZED)

        if request.method == "POST":
            try:
                photo = Photo(userprofile=request.user.userprofile, image=request.data["image"])
                photo.save()
                return Response({"message": "Post Successful"})
            except:
                return Response({"error": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

        photos = []
        for photo in Photo.objects.all():
            photos.append({
                    "id": photo.id,
                    "userprofile": {
                        "id": photo.userprofile.id,
                        "profile_picture": photo.userprofile.profile_picture.url,
                        "username": photo.userprofile.user.username
                    },
                    "image": photo.image.url
                })
        response = {"photos" : photos, "user": request.user.username}
        return Response(response, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=["GET"])
    def home(self, request):
        photos = []
        for photo in Photo.objects.filter(userprofile=request.user.userprofile):
            photos.append({
                    "id": photo.id,
                    "image": photo.image.url
                })
        response = {"photos" : photos, "user": { "username": request.user.username, "profile_picture": request.user.userprofile.profile_picture.url }}
        return Response(response, status=status.HTTP_200_OK)