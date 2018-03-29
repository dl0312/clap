from django.contrib import admin
from .models import Post, Genre, Image
from mptt.admin import MPTTModelAdmin
from mptt.admin import DraggableMPTTAdmin

class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'lft', 'rght', 'tree_id', 'parent')

class AdMPTTModelAdmin(MPTTModelAdmin):
    list_display = ('name', 'lft', 'rght', 'tree_id', 'parent')

admin.site.register(Post)
#admin.site.register(Genre, AdMPTTModelAdmin)
admin.site.register(Image)
admin.site.register(
    Genre,
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

# Register your models here.


