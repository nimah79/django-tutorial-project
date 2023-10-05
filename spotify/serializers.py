from rest_framework import serializers


from spotify.models import Post


class PostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    content = serializers.CharField()


    def create(self, data):
        return Post.objects.create(**data)


    def update(self, post, data):
        post.title = data.get('title', post.title)
        # ...
        post.save()
        return post


    def valiate(self, data):
        if len(data.get('title')) > 255:
            raise serializers.ValidationError('Title length must not exceed 255 characters')

        return data


    #def validate_title(self, value):
    #    # Validation logic
