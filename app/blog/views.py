""" TEST API METHODS """
import json

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.generic import View

from .models import Blog as BlogModel
from .mixins import HttpResponseMixin, JsonResponseMixin


def getBlogPostsJV(request):
    """ JSON View -> GET Method """
    data = {
        "name": "Test data",
        "content": "Django API from HttpResponse"
    }
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


class BlogPostViews(View):
    """ Class-Based View """

    def get(self, request, *args, **kwargs):
        data = {
            "name": "Test data",
            "content": "Django API from BlogPostViews"
        }
        return JsonResponse(data)


class BlogPostMixin(JsonResponseMixin, View):
    """ Class-Based View using JsonResponseMixin """

    def get(self, request, *args, **kwargs):
        data = {
            "name": "Test data",
            "content": "Django API from BlogPostMixin"
        }
        return self.render_to_json_response(data)


class SerializedDetailView(View):
    def get(self, request, *args, **kwargs):
        # Get particular id
        obj = BlogModel.objects.get(id=1)
        json_data = obj.serialize()
        return HttpResponse(json_data, content_type='application/json')


class SerializedListView(View):
    def get(self, request, *args, **kwargs):
        qs = BlogModel.objects.all()
        json_data = BlogModel.objects.all().serialize()
        return HttpResponse(json_data, content_type='application/json')
