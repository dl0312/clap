from rest_framework import serializers
from rest_auth.registration.serializers import RegisterSerializer
from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from . import models
from taggit_serializer.serializers import (TagListSerializerField, TaggitSerializer)

class SmallImageSerializer(serializers.ModelSerializer):

    """ Used for the notifications """

    class Meta:
        model = models.Image
        fields = (
            'image',
        )

class CountPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'comment_count',
            'clap_count',
        )

class FeedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'username',
            'profile_image'
        )

class CommentSerializer(serializers.ModelSerializer):

    creator = FeedUserSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'message',
            'creator',
        )

class ClapSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Clap
        fields = '__all__'

class MpttSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = (
            'name',
        )

class PostSerializer(TaggitSerializer, serializers.ModelSerializer):

    comments = CommentSerializer(many=True)
    creator = FeedUserSerializer()
    tags = TagListSerializerField()
    is_claped = serializers.SerializerMethodField()
    category = MpttSerializer()

    class Meta:
        model = models.Post
        fields = (
            'id',
            'category',
            'title',
            'body',
            'comments',
            'clap_count',
            'creator',
            'tags',
            'natural_time',
            'is_claped',
        )

    def get_is_claped(self, obj):
        if 'request' in self.context:
            request = self.context['request']
            try:
                models.Clap.objects.get(creator__id=request.user.id, post__id=obj.id)
                return True
            except models.Clap.DoesNotExist:
                return False
        return False

class InputImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = (
            'post',
            'image',
        )



class UserProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.User
        fields = ('profile_image', 'username', 'bio')