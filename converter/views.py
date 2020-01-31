import os

from PIL import Image
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template import loader

from converter.backend.convert import create_wallpaper
from converter.backend.resolutions import HD_1080
from converter.backend.resolutions import resolution
from converter.forms import ImageForm


def add_suffix(filename, suffix):
    tokens = filename.split('.')
    name, extension = tokens[0], tokens[-1]
    return f"{name}-{suffix}.{extension}"


def index(request):
    template = loader.get_template('converter/index.html')

    try:
        if request.method == 'POST' and request.FILES['image']:
            image = Image.open(request.FILES['image'])
            filename = request.FILES['image'].name

            # TODO: Choose resolution
            if 'width' in request.POST and 'height' in request.POST:
                width, height = request.POST['width'], request.POST['height']
                res = resolution(f"{width}x{height}", int(width), int(height))
            else:
                res = HD_1080

            # TODO: Choose color, None will default to most common color
            color = None

            wallpaper = create_wallpaper(image, res, color)
            wallpaper_filename = add_suffix(filename, res.name)

            fs = FileSystemStorage()

            wallpaper_path = os.path.join(fs.base_location, wallpaper_filename)
            wallpaper.save(wallpaper_path)

            context = {
                "wallpaper_created": True,
                "wallpaper_path": os.path.join(settings.MEDIA_URL, wallpaper_filename),
                "form": ImageForm(),
            }

            return HttpResponse(template.render(context, request))
    except:
        context = {"errors": True}
        return HttpResponse(template.render(context, request))

    context = {
        "form": ImageForm()
    }
    return HttpResponse(template.render(context, request))
