from django.contrib import admin

from .models import Categories, Post, PostImage, Comment


class ImageInLine(admin.TabularInline):
    model = PostImage
    extra = 3
    fields = ['image']


class PostAdmin(admin.ModelAdmin):
    inlines = [
        ImageInLine
    ]
    list_display = ('uuid', 'title', 'price')
    list_display_links = ('uuid', 'title')


admin.site.register(Categories)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
