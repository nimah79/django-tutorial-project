from django import forms


from spotify.models import Post


class CreatePostForm(forms.ModelForm):
	# def __init__(self, *args, **kwargs):
	# 	super(CreatePostForm, self).__init__(*args, **kwargs)
	# 	self.fields['content'].required = False

	class Meta:
		model = Post
		fields = ('author', 'title', 'content')
