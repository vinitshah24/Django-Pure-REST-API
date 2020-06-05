from django import forms

from .models import Blog as BlogModel


class BlogForm(forms.ModelForm):
    class Meta:
        model = BlogModel
        fields = ['user', 'content', 'image']

    # OVERRIDING - ModelForm.clean() method
    def clean(self, *args, **kwargs):
        data = self.cleaned_data
        content = data.get('content', None)
        if content == "":
            content = None
        image = data.get("image", None)
        if content is None and image is None:
            raise forms.ValidationError('Content or image is required.')
        return super().clean(*args, **kwargs)
