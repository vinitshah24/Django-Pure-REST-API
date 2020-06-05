import json
from django.views.generic import View
from django.http import HttpResponse

from blog.mixins import HttpResponseMixin
from blog.forms import BlogForm
from blog.models import Blog as BlogModel

from .mixins import CSRFExemptMixin
from .utils import is_vaid_json


class BlogDetailViews(HttpResponseMixin, CSRFExemptMixin, View):

    def get_id_details(self, id=None):
        query_set = BlogModel.objects.filter(id=id)
        return query_set.first() if query_set.count() == 1 else None

    # GET the blog item
    def get(self, request, id, *args, **kwargs):
        blog_item = self.get_id_details(id=id)
        if blog_item is None:
            error_data = json.dumps({"message": "Item not found"})
            return self.render_to_response(error_data, status=404)
        json_data = blog_item.serialize()
        return self.render_to_response(json_data)

    def post(self, request, *args, **kwargs):
        json_data = json.dumps({"message": "Not allowed, Use /api/blog/"})
        return self.render_to_response(json_data, status=403)

    # UPDATE the blog item
    def put(self, request, id, *args, **kwargs):
        # Parse the request body for updating the blog item
        valid_json = is_vaid_json(request.body)
        # Validation for invalid JSON body
        if not valid_json:
            error_data = json.dumps({"message": "Invalid JSON data!"})
            return self.render_to_response(error_data, status=400)
        original_data = self.get_id_details(id=id)
        # Check if the data exists in the database with that ID
        if original_data is None:
            error_data = json.dumps(
                {"message": "Item does not exists with that ID!"})
            return self.render_to_response(error_data, status=404)
        # serialize the original data from the database to JSON
        og_data = json.loads(original_data.serialize())
        passed_data = json.loads(request.body)
        for key, value in passed_data.items():
            og_data[key] = value
        form = BlogForm(og_data, instance=original_data)
        # If everything is valid
        if form.is_valid():
            # Save the data
            original_data = form.save(commit=True)
            updated_data = json.dumps(og_data)
            return self.render_to_response(updated_data, status=201)
            # If form validation fails
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, status=400)
        json_data = json.dumps({"message": "Something went wrong!"})
        return self.render_to_response(json_data)

    # DELETE the blog item
    def delete(self, request, id, *args, **kwargs):
        original_data = self.get_id_details(id=id)
        # If no data is found then the ID does not exists
        if original_data is None:
            error_data = json.dumps({"message": "Item not found!"})
            return self.render_to_response(error_data, status=404)
        # Else delete the item
        deleted_, item_deleted = original_data.delete()
        if deleted_ == 1:
            json_data = json.dumps({"message": "Successfully deleted."})
            return self.render_to_response(json_data, status=200)
        error_data = json.dumps({"message": "Item failed to delete"})
        return self.render_to_response(error_data, status=400)


class BlogListViews(HttpResponseMixin, CSRFExemptMixin, View):

    def get_queryset(self):
        qs = BlogModel.objects.all()
        self.queryset = qs
        return qs

    def get_id_list(self, id=None):
        if id is None:
            return None
        query_set = self.get_queryset().filter(id=id)
        return query_set.first() if query_set.count() == 1 else None

    def get(self, request, *args, **kwargs):
        # Get the data from JSON body
        data = json.loads(request.body)
        # Get the id from the URI
        passed_id = data.get("id", None)
        # If the id is passed
        if passed_id is not None:
            obj = self.get_id_list(id=passed_id)
            if obj is None:
                error_data = json.dumps({"message": "Item not found!"})
                return self.render_to_response(error_data, status=404)
            json_data = obj.serialize()
            return self.render_to_response(json_data)
        # If there is no id, show full list
        else:
            qs = self.get_queryset()
            json_data = qs.serialize()
            return self.render_to_response(json_data)

    def post(self, request, *args, **kwargs):
        # Check if the request body is valid JSON
        valid_json = is_vaid_json(request.body)
        # IF not a valid JSON, return error message
        if not valid_json:
            error_data = json.dumps({"message": "Invalid JSON body!"})
            return self.render_to_response(error_data, status=400)
        data = json.loads(request.body)
        form = BlogForm(data)
        # If data is valid, save the data
        if form.is_valid():
            obj = form.save(commit=True)
            obj_data = obj.serialize()
            return self.render_to_response(obj_data, status=201)
        # Else send the error message
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, status=400)
        data = {"message": "Invalid data!"}
        return self.render_to_response(data, status=400)

    def put(self, request, *args, **kwargs):
        # Check if the request body is valid JSON
        valid_json = is_vaid_json(request.body)
        # If not valid, return with error message
        if not valid_json:
            error_data = json.dumps({"message": "Invalid JSON body!"})
            return self.render_to_response(error_data, status=400)
        passed_data = json.loads(request.body)
        passed_id = passed_data.get('id', None)
        # Check if the ID is passed in the body
        if not passed_id:
            error_data = json.dumps({"message": "ID required for Update!"})
            return self.render_to_response(error_data, status=400)
        # Get the original data from the database
        original_data = self.get_id_list(id=passed_id)
        # If the data is not found in database, return error message
        if original_data is None:
            error_data = json.dumps({"message": "No item to update!"})
            return self.render_to_response(error_data, status=404)
        # Serialize it to JSON
        data = json.loads(original_data.serialize())
        # Update the og data to updated data
        for key, value in passed_data.items():
            data[key] = value
        # Send it to the form and validate the data
        form = BlogForm(data, instance=original_data)
        # If valid, save to the database
        if form.is_valid():
            original_data = form.save(commit=True)
            obj_data = json.dumps(data)
            return self.render_to_response(obj_data, status=201)
        # Else return with error message
        if form.errors:
            data = json.dumps(form.errors)
            return self.render_to_response(data, status=400)
        # Base case for any unknown error
        json_data = json.dumps({"message": "Something went wrong!"})
        return self.render_to_response(json_data)

    def delete(self, request, *args, **kwargs):
        # Check if the request body is valid JSON
        valid_json = is_vaid_json(request.body)
        # If not valid, return with error message
        if not valid_json:
            error_data = json.dumps({"message": "Invalid JSON body!"})
            return self.render_to_response(error_data, status=400)
        passed_data = json.loads(request.body)
        passed_id = passed_data.get('id', None)
        # Check if the ID is passed in the body
        if not passed_id:
            error_data = json.dumps({"message": "ID required for deletion!"})
            return self.render_to_response(error_data, status=400)
        # Fetch the data with that id
        obj = self.get_id_list(id=passed_id)
        if obj is None:
            error_data = json.dumps({"message": "Item not found"})
            return self.render_to_response(error_data, status=404)
        # Delete the data with that ID
        deleted_, item_deleted = obj.delete()
        if deleted_ == 1:
            json_data = json.dumps({"message": "Successfully deleted."})
            return self.render_to_response(json_data, status=200)
        error_data = json.dumps({"message": "Something went wrong!"})
        return self.render_to_response(error_data, status=400)
