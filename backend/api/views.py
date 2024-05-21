from rest_framework import views, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication

from api.serializers import PersonalLetterCreatorSerializer, TokenSerializer, UserSerializer
from api.models import PersonalLetter
from rest_framework.permissions import AllowAny

# Vad man ska få från varje endpoint

class LetterCreatorView(views.APIView):
    serializer_class = PersonalLetterCreatorSerializer
    authentication_classes = []
    permission_classes = [AllowAny]
    # TokenAuthentication

    # Om man gör en get requst

    def get(self, request, format=None):
        query_set = PersonalLetter.objects.all()
        serializer = self.serializer_class(query_set, many=True)
        return Response(serializer.data)
    
    # Om man gör en post requst
    
    def post(self, request, format=None):
        print('request data', request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(views.APIView):
    serializer_class = UserSerializer

    def get(self, request, format=None):
        query_set = User.objects.all()
        serializer = self.serializer_class(query_set, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        # Lite debugging som jag gjorde
        print("Received Headers:", request.headers)  
        print("Received Body:", request.body.decode('utf-8'))

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TokenView(ObtainAuthToken):
    serializer_class = TokenSerializer
