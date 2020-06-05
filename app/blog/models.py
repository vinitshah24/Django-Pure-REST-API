import json

from django.core.serializers import serialize
from django.conf import settings
from django.db import models


def upload_image(instance, filename):
    return "blog/{user}/{filename}".format(user=instance.user, filename=filename)


class BlogQuerySet(models.QuerySet):
    def serializeLongerWay(self):
        query_set = self
        final_array = []
        for obj in query_set:
            stuct = json.loads(obj.serialize())
            final_array.append(stuct)
        return json.dumps(final_array)

    def serialize(self):
        list_values = list(self.values("user", "content", "image", "id"))
        return json.dumps(list_values)

# https://docs.djangoproject.com/en/dev/topics/db/managers/#manager-names
# Used for adding methods to the Model so it can be used like: ModelName.objects.methodInManager()
class BlogManager(models.Manager):

    # Serializing the data before returning
    def get_queryset(self):
        return BlogQuerySet(self.model, using=self._db)


class Blog(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    content = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to=upload_image, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # objects is default name. Can name anything else [Remember to use it while quering]
    # https://stackoverflow.com/questions/4455330/
    objects = BlogManager()

    def __str__(self):
        return self.content or ""

    def serialize(self):
        try:
            image = self.image.url
        except:
            image = ""
        data = {
            "id": self.id,
            "content": self.content,
            "user": self.user.id,
            "image": image
        }
        data = json.dumps(data)
        return data
