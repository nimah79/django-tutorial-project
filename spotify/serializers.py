from rest_framework import serializers


from spotify.models import Post


class PostSerializer(serializers.Serializer):
	title = serializers.CharField(max_length=255)
    content = serializers.TextField()


    def create(self, data):
    	return Post.objects.create(**data)


    def update(self, post, data):
    	post.title = data.get('title', post.title)
    	# ...
    	post.save()
    	return post


    def validate_title(self, value):
    	# Validation logic
