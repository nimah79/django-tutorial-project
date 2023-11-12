from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class ModelWithTimestamps(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()

    def is_older_than(self, age):
        return self.age > age

    def __str__(self):
        return self.first_name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=255)


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Many to many: authors = models.ManyToManyField(User)
    # One to one: author = models.OneToOneField(User)

    class Meta:
        permissions = [
            ('change_post_content', 'Can change post content')
        ]

    def __str__(self):
        return f'{self.id}. {self.title}'


class JwtIdentifier(models.Model):
    identifier = models.CharField(max_length=255)


class Country(ModelWithTimestamps):
    name = models.CharField(max_length=255)


class City(ModelWithTimestamps):
    name = models.CharField(max_length=255)
    country = models.ForeignKey(
        Country,
        related_name='cities',
        on_delete=models.CASCADE
    )


class Like(models.Model):
    type = models.BooleanField()
    user = models.ForeignKey(
        User,
        related_name='likes',
        on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Rate(models.Model):
    type = models.BooleanField()
    user = models.ForeignKey(
        User,
        related_name='rates',
        on_delete=models.CASCADE
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class Artist(ModelWithTimestamps):
    name = models.CharField(max_length=255)
    image = models.TextField()
    likes = GenericRelation(Like)
    rates = GenericRelation(Rate)


class Genre(ModelWithTimestamps):
    name = models.CharField(max_length=255)


class Album(ModelWithTimestamps):
    name = models.CharField(max_length=255)
    release_datetime = models.DateTimeField()
    image = models.TextField()
    genres = models.ManyToManyField(Genre, related_name='albums')
    likes = GenericRelation(Like)
    rates = GenericRelation(Rate)


class Cover(ModelWithTimestamps):
    image = models.TextField()
    album = models.ForeignKey(
        Album,
        related_name='covers',
        on_delete=models.CASCADE
    )
    likes = GenericRelation(Like)
    rates = GenericRelation(Rate)


class Track(ModelWithTimestamps):
    name = models.CharField(max_length=255)
    duration = models.PositiveIntegerField()
    lyrics = models.TextField(blank=True, null=True)
    path_128 = models.TextField()
    path_320 = models.TextField()
    album = models.ForeignKey(
        Album,
        blank=True,
        null=True,
        related_name='tracks',
        on_delete=models.CASCADE
    )
    artist = models.ForeignKey(
        Artist,
        related_name='tracks',
        on_delete=models.CASCADE
    )
    likes = GenericRelation(Like)
    rates = GenericRelation(Rate)


class Playlist(ModelWithTimestamps):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        User,
        related_name='playlists',
        on_delete=models.CASCADE
    )
    tracks = models.ManyToManyField(Track, through='PlaylistTrack')
    likes = GenericRelation(Like)
    rates = GenericRelation(Rate)


class PlaylistTrack(ModelWithTimestamps):
    playlist = models.ForeignKey(
        Playlist,
        related_name='playlist_tracks',
        on_delete=models.CASCADE
    )
    track = models.ForeignKey(
        Track,
        related_name='playlist_tracks',
        on_delete=models.CASCADE
    )


class Subscription(ModelWithTimestamps):
    title = models.CharField(max_length=255)
    duration = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)


class UserSubscription(ModelWithTimestamps):
    user = models.ForeignKey(
        User,
        related_name='user_subscriptions',
        on_delete=models.CASCADE
    )
    subscription = models.ForeignKey(
        Subscription,
        related_name='user_subscriptions',
        on_delete=models.CASCADE
    )


class Coupon(ModelWithTimestamps):
    COUPON_TYPES = (
        ('p', 'percent'),
        ('a', 'amount'),
    )
    title = models.CharField(max_length=255)
    type = models.CharField(max_length=1, choices=COUPON_TYPES)
    value = models.PositiveIntegerField()
    max_amount = models.PositiveIntegerField(blank=True, null=True)
    max_usage_count = models.PositiveIntegerField(blank=True, null=True)
    max_usage_count_per_user = models.PositiveIntegerField(blank=True, null=True)
    only_for_first_transaction = models.BooleanField(default=False)
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_until = models.DateTimeField(blank=True, null=True)


class Voucher(ModelWithTimestamps):
    subscription = models.ForeignKey(
        Subscription,
        related_name='vouchers',
        on_delete=models.CASCADE
    )


class VoucherRedeem(ModelWithTimestamps):
    user = models.ForeignKey(
        User,
        related_name='voucher_redeems',
        on_delete=models.CASCADE
    )
    voucher = models.ForeignKey(
        Voucher,
        related_name='voucher_redeems',
        on_delete=models.CASCADE
    )
