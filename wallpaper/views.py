import io
import logging
import os
import sys

from PIL import Image
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from wallpaper.backend.convert import create_wallpaper
from wallpaper.backend.resolutions import HD_1080
from wallpaper.backend.resolutions import resolution
from wallpaper.backend.util import get_final_filename
from wallpaper.backend.util import get_image_format
from wallpaper.forms import ImageForm
from wallpaper.models import Upload

log = logging.getLogger("app")


def redirect_wallpaper(request):
    log.info("Redirecting root to /wallpaper...")
    return redirect('/wallpaper')


def index(request):
    log.info("views.index called")
    template = loader.get_template('wallpaper/index.html')

    try:
        if request.method == 'POST' and request.FILES['image']:
            log.info("Starting to handle POST request with image...")
            image = Image.open(request.FILES['image'])
            filename = request.FILES['image'].name

            # TODO: Choose resolution
            if 'width' in request.POST and 'height' in request.POST:
                width, height = request.POST['width'], request.POST['height']
                res = resolution(f"{width}x{height}", int(width), int(height))
                log.info(f"Resolution given:{res}")
            else:
                res = HD_1080
                log.info(f"Resolution not given, using default:{res}")

            # TODO: Choose color, None will default to most common color
            color = None

            wallpaper = create_wallpaper(image, res, color)
            wallpaper_filename = get_final_filename(filename, res.name)
            log.info(f"Final wallpaper_filename: {wallpaper_filename}")

            if settings.USE_S3:
                log.info("Converting wallpaper to bytes...")
                bytes = io.BytesIO()  # this is a file object
                wallpaper.save(bytes, get_image_format(wallpaper_filename))
                file = InMemoryUploadedFile(bytes, None, wallpaper_filename, 'image/jpeg',
                                            sys.getsizeof(bytes), None)

                log.info("Uploading wallpaper to S3...")
                upload = Upload(file=file)
                upload.save()
                log.info("Done")
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
        log.info(f"Exception caught while handling POST request: {e}")
        context = {
            "errors": True
        }
        return HttpResponse(template.render(context, request))

    log.info(f"Responding to GET request...")
    context = {
        "form": ImageForm()
    }
    return HttpResponse(template.render(context, request))
