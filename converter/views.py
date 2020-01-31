import io
import os
import sys

from PIL import Image
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from converter.backend.convert import create_wallpaper
from converter.backend.resolutions import HD_1080
from converter.backend.resolutions import resolution
from converter.backend.util import get_final_filename
from converter.forms import ImageForm
from converter.models import Upload


def redirect_wallpaper(request):
    return redirect('/wallpaper')


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
            wallpaper_filename = get_final_filename(filename, res.name)
            print("wallpaper_filename:", wallpaper_filename)

            if settings.USE_S3:
                bytes = io.BytesIO()  # this is a file object
                wallpaper.save(bytes, "JPEG")
                file = InMemoryUploadedFile(bytes, None, wallpaper_filename, 'image/jpeg',
                                            sys.getsizeof(bytes), None)

                print("UPLOADING TO S3")
                upload = Upload(file=file)
                print("Upload created")
                upload.save()
                print("Upload saved")
            else:
                fs = FileSystemStorage()
                wallpaper_path = os.path.join(fs.base_location, wallpaper_filename)
                wallpaper.save(wallpaper_path)

            context = {
                "wallpaper_created": True,
                "wallpaper_path": os.path.join(settings.MEDIA_URL, wallpaper_filename),
                "form": ImageForm(),
            }

            return HttpResponse(template.render(context, request))
    except Exception as e:
        return HttpResponse(template.render(context, request))

    context = {
        "form": ImageForm()
    }
    return HttpResponse(template.render(context, request))
