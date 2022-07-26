from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    # list of model properties that we want to show in the admin interface
    list_display = ("pk", "text", "pub_date", "author")

    # interface for searching in the text of posts
    search_fields = ("text",)

    # ability to filter by date
    list_filter = ("pub_date",)

    # this property will work for all empty columns
    empty_value_display = "-empty-"


# assign the PostAdmin class as a configuration source for Post model
admin.site.register(Post, PostAdmin)
