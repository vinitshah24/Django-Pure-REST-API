from django.urls import path

from .views import BlogDetailViews, BlogListViews

urlpatterns = [
    path('<id>', BlogDetailViews.as_view()),
    path('', BlogListViews.as_view()),
]
