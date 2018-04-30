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
        model = models.Post
        fields = (
            'id',
            'title',
            'comment_count',
            'clap_count',
        )

class GameSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Game
        fields = (
            'title',
            'icon'
        )

class FeedUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        fields = (
            'username',
            'profile_image',
            'certification',
        )

class ListUserSerializer(serializers.ModelSerializer):

    following = serializers.SerializerMethodField()

    class Meta:
        model = models.User
        fields = (
            'id',
            'profile_image',
            'username',
            'name',
            'following'
        )
    
    def get_following(self,obj):
        if 'request' in self.context:
            request = self.context['request']
            if obj in request.user.following.all():
                return True
            return False

class UserProfileSerializer(serializers.ModelSerializer):
    
    posts = CountPostSerializer(many=True, read_only=True)
    post_count = serializers.ReadOnlyField()
    followers_count = serializers.ReadOnlyField()
    following_count = serializers.ReadOnlyField()
    game = GameSerializer(many=True)

    class Meta:
        model = models.User
        fields = (
            'profile_image',
            'username',
            'name',
            'certification',
            'game',
            'bio',
            'post_count',
            'followers_count',
            'following_count',
            'posts'
        )

class SignUpSerializer(RegisterSerializer):

    name = serializers.CharField(required=True, write_only=True)

    def get_cleaned_data(self):
        return {
            'name': self.validated_data.get('name', ''),
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'email': self.validated_data.get('email', '')
        }
    
    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        setup_user_email(request, user, [])
        user.save()
        return user

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
            'mptt_level'
        )

class ChildrenSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = (
            'name',
            'get_ancestors()'
        )

class SimplePostSerializer(TaggitSerializer, serializers.ModelSerializer):

    creator = FeedUserSerializer()
    is_claped = serializers.SerializerMethodField()
    category = MpttSerializer()

    class Meta:
        model = models.Post
        fields = (
            'id',
            'category',
            'title',
            'comment_count',
            'clap_count',
            'creator',
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

class InputPostSerializer(serializers.ModelSerializer):
    
    category = MpttSerializer()

    class Meta:
        model = models.Post
        fields = (
            'category',
            'title',
            'body',
        )

class WikiImageSerializer(serializers.ModelSerializer):
    
    category = MpttSerializer()

    class Meta:
        model = models.WikiImage
        fields = (
            'category',
            'image',
        )


class InputImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Image
        fields = (
            'image',
        )

class NotificationSerializer(serializers.ModelSerializer):

    creator = ListUserSerializer()
    post = SimplePostSerializer()

    class Meta:
        model = models.Notification
        fields = '__all__'



