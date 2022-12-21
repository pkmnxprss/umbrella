from django.contrib import admin

from .models import Post, Group


class PostAdmin(admin.ModelAdmin):
    # List of model properties that we want to show in the admin interface
    list_display = ("pk", "text", "pub_date", "author")

    # Interface for searching in the text of posts
    search_fields = ("text",)

    # Ability to filter by date
    list_filter = ("pub_date",)

    # This property will work for all empty columns
    empty_value_display = "-empty-"


# Assign the PostAdmin class as a configuration source for Post model
admin.site.register(Post, PostAdmin)


class GroupAdmin(admin.ModelAdmin):
    # List of model properties that we want to show in the admin interface
    list_display = ("title", "slug", "description")

    # This property will work for all empty columns
    empty_value_display = "-empty-"


# Assign the PostAdmin class as a configuration source for Post model
admin.site.register(Group, GroupAdmin)

