from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    age = models.IntegerField()


class User(models.Model):
    GENDER_CHOICES = (
        ('m', 'male'),
        ('f', 'female'),
    )

    username = models.CharField(max_length=255)
    gender = models.CharField(
        max_length=255,
        choices=GENDER_CHOICES,
        default='f',
    )
    email = models.EmailField()
    last_visit = models.DateTimeField()
    # BooleanField
    # DateField
    # FloatField
    # TextField

    def toggle_gender(self):
        self.gender = 'f' if self.gender == 'm' else 'm'
        self.save()


class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Many to many: authors = models.ManyToManyField(User)
    # One to one: author = models.OneToOneField(User)
