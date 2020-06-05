from django.contrib import admin
from django.contrib.auth import views

from django.urls import path, include

from blog.views import (
    getBlogPostsJV,
    BlogPostViews,
    BlogPostMixin,
    SerializedDetailView,
    SerializedListView,
)

urlpatterns = [
    # Admin page
    path('admin/', admin.site.urls),
    # Main API
    path('api/blog/', include('blog.api.urls')),
    # Method
    path('method', getBlogPostsJV),
    # Classes
    path('view', BlogPostViews.as_view()),
    path('mixin', BlogPostMixin.as_view()),
    path('serialize/user/1', SerializedDetailView.as_view()),
    path('serialize/all', SerializedListView.as_view()),
]
