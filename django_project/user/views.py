from rest_framework import serializers, viewsets
import json
from rest_framework.authtoken.models import Token

from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password

from .models import CustomUser


DEFAULT_PASSWORD = "pass,123"

# Create your views here.
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ["id", "name", "email", "phone", "password"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def get_queryset(self):
        q = super().get_queryset()

        if not q:
            # load user from json
            with open("user_data.json", 'r') as f:
                data = json.loads(f.read())

                for user in data:
                    u = CustomUser(name=user['name'], email=user['email'], phone=user['phone'])
                    u.set_password(DEFAULT_PASSWORD)
                    u.save()
            
            return super().get_queryset()

        return q


class LoginSerialiser(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField()


class LoginViewSet(viewsets.ViewSet):

    queryset = CustomUser.objects.all()
    serializer_class = LoginSerialiser

    def create(self, request, *args, **kwargs):
        serializer = LoginSerialiser(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = CustomUser.objects.filter(email=email).first()

        if user and user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key
            })
        else:
            return Response({
                "message": "Wrong credential"
            })
