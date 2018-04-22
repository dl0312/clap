from django.contrib import admin
from .models import User, Post, Category, Image
from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'lft', 'rght', 'tree_id', 'parent')

class AdMPTTModelAdmin(MPTTModelAdmin):
    list_display = ('name', 'lft', 'rght', 'tree_id', 'parent')

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Image)
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