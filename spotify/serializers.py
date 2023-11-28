import uuid

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from spotify.models import *


class LikedObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.__str__()


class RatedObjectRelatedField(serializers.RelatedField):
    def to_representation(self, value):
        return value.__str__()


class LikeableMixin:
    likes = LikedObjectRelatedField(many=True, queryset=Like.objects.all())


class RateableMixin:
    rates = RatedObjectRelatedField(many=True, queryset=Rate.objects.all())


class LikeableAndRateableMixin(LikeableMixin, RateableMixin):
    pass


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


class CountrySerializer(serializers.ModelSerializer):
    cities = serializers.StringRelatedField(many=True)

    class Meta:
        model = Country
        fields = ["id", "name", "cities"]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name", "country"]


class ArtistSerializer(serializers.ModelSerializer, LikeableAndRateableMixin):
    class Meta:
        model = Artist
        fields = "__all__"


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = "__all__"


class AlbumSerializer(serializers.ModelSerializer, LikeableAndRateableMixin):
    covers = serializers.StringRelatedField(many=True)

    class Meta:
        model = Album
        fields = "__all__"


class CoverSerializer(serializers.ModelSerializer, LikeableAndRateableMixin):
    class Meta:
        model = Cover
        fields = "__all__"


class TrackSerializer(serializers.ModelSerializer, LikeableAndRateableMixin):
    class Meta:
        model = Track
        fields = "__all__"


class PlaylistSerializer(serializers.ModelSerializer, LikeableAndRateableMixin):
    class Meta:
        model = Playlist
        fields = "__all__"


class PlaylistTrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaylistTrack
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class UserSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSubscription
        fields = "__all__"


class CouponSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coupon
        fields = "__all__"


class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voucher
        fields = "__all__"


class VoucherRedeemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoucherRedeem
        fields = "__all__"


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
