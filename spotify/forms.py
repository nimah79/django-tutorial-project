from django import forms
from django.contrib.auth.forms import UserCreationForm


from spotify.models import Post, Profile, User


class CreatePostForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    # 	super(CreatePostForm, self).__init__(*args, **kwargs)
    # 	self.fields['content'].required = False

    class Meta:
        model = Post
        fields = ("author", "title", "content")


class ContactForm(forms.Form):
    name = forms.CharField()
    message = forms.CharField(widget=forms.Textarea)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass


class SignUpForm(UserCreationForm):
    phone_number = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ("username", "phone_number", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=commit)
        Profile.objects.create(user=user, phone_number=self.data["phone_number"])
        return user
