from django.contrib import admin

from .models import Blog as BlogModel

# Register the table Blogs
admin.site.register(BlogModel)
