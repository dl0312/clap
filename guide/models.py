from django.db import models
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from taggit.managers import TaggableManager
from django.urls import reverse
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify

def upload_location(instance, filename):
    return "%s/%s" %(instance.id, filename)

class TimeStampeModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Category(MPTTModel):
    name = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='children', db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'pk': self.pk, })

    @property
    def get_images(self):
        return self.images.all()

    @property
    def get_posts(self):
        return self.posts.all() 

    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['name']

@python_2_unicode_compatible
class Game(TimeStampeModel):

    """ Game Model """
    title = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='games')
    logo = models.ImageField(upload_to='photos/%Y/%m/%d',verbose_name='Logo',)
    icon = models.ImageField(upload_to='photos/%Y/%m/%d',verbose_name='Icon',)

    def __str__(self):
        return self.title

@python_2_unicode_compatible
class Achievement(TimeStampeModel):

    """ Achievement Model """

    name = models.CharField(max_length=64)
    condition = models.CharField(max_length=128,null=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class User(AbstractUser):

    """ User Model """

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('not-specified', 'Not specified')
    )

    profile_image = models.ImageField(null=True)
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    bio = models.TextField(null=True)
    phone = models.CharField(max_length=140,null=True)
    game = models.ManyToManyField(Game, null=True)
    achievement = models.ManyToManyField(Achievement, null=True)
    gender = models.CharField(max_length=80, choices=GENDER_CHOICES, null=True)
    followers = models.ManyToManyField("self", blank=True)
    following = models.ManyToManyField("self", blank=True)
    exp = models.IntegerField(default=0)
    clap = models.IntegerField(default=0)
    certification = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def post_count(self):
        return self.posts.all().count()

    @property
    def followers_count(self):
        return self.followers.all().count()

    @property
    def following_count(self):
        return self.following.all().count()



@python_2_unicode_compatible
class Post(TimeStampeModel):

    """ Post Model """

    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='posts')
    body = models.TextField()
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='posts')
    tags = TaggableManager()
    view = models.IntegerField(default=0)

    @property
    def clap_count(self):
        return self.claps.all().count()

    @property
    def comment_count(self):
        return self.comments.all().count()

    @property
    def natural_time(self):
        return naturaltime(self.created_at)

    @property
    def ancestors(self):
        return self.category.get_ancestors()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

@python_2_unicode_compatible
class Comment(TimeStampeModel):

    """ Comment Model """

    message = models.TextField()
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.message

@python_2_unicode_compatible
class Clap(TimeStampeModel):

    """ Like Model """

    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='claps')
    post = models.ForeignKey(Post, null=True, on_delete=models.CASCADE, related_name='claps')

    def __str__(self):
        return 'User: {} - Post: {}'.format(self.creator.username, self.post.title)

@python_2_unicode_compatible
class Image(TimeStampeModel):

    """ Image Model """

    image = models.ImageField(upload_to='photos/%Y/%m/%d',verbose_name='Image',)

    @property
    def natural_time(self):
        return naturaltime(self.created_at)


    def __str__(self):
        return self.image.url

    class Meta:
        ordering = ['-created_at']


class WikiImage(TimeStampeModel):

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='images')
    image = models.ImageField(upload_to='photos/%Y/%m/%d',verbose_name='Image',)

    @property
    def natural_time(self):
        return naturaltime(self.created_at)


    def __str__(self):
        return '{} - {}'.format(self.image)

    class Meta:
        ordering = ['-created_at']


class Notification(TimeStampeModel):

    TYPE_CHOICES = (
        ('clap', 'Clap'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('guide','Guide')
    )

    creator = models.ForeignKey(User, on_delete=models.PROTECT, related_name='creator')
    to = models.ForeignKey(User, on_delete=models.PROTECT, related_name='to')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(null=True,blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return 'From: {} - To: {}'.format(self.creator, self.to)