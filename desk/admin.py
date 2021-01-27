from django.contrib import admin

from .models import Category, Post, PostImage, Comment


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


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
