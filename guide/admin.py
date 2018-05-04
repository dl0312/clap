from django.contrib import admin
from .models import *
from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'lft', 'rght', 'tree_id', 'parent')

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username')


class AdMPTTModelAdmin(MPTTModelAdmin):
    list_display = ('name', 'lft', 'rght', 'tree_id', 'parent')

admin.site.register(User,UserAdmin)
admin.site.register(Game)
admin.site.register(Achievement)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Clap)
admin.site.register(Image)
admin.site.register(WikiImage)
admin.site.register(Notification)
admin.site.register(
    Category,
    DraggableMPTTAdmin,
    list_display=(
        'tree_actions',
        'indented_title',
        'name',
        # ...more fields if you feel like it...
    ),
    list_display_links=(
        'indented_title',
    ),
)