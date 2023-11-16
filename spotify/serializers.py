import uuid

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from spotify.models import *


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token["identifier"] = str(uuid.uuid4())

        identifier = JwtIdentifier(identifier=token["identifier"])
        identifier.save()

        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author"]


class DynamicFieldsSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop("fields", None)
        super().__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class CountrySerializer(DynamicFieldsSerializer):
    cities = serializers.StringRelatedField(many=True)

    class Meta:
        model = Country
        fields = ["id", "name", "cities"]


class CitySerializer(serializers.ModelSerializer):
    country = CountrySerializer(fields=("id", "name"))

    class Meta:
        model = City
        fields = ["id", "name", "country"]


class LikedObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.__str__()


class ArtistSerializer(serializers.ModelSerializer):
    likes = LikedObjectRelatedField(many=True, queryset=Like.objects.all())

    class Meta:
        model = Artist
        fields = "__all__"
