from django.forms import Form
from django.forms import ImageField
from django.forms import IntegerField


class ImageForm(Form):
    image = ImageField()
    width = IntegerField()
    height = IntegerField()
