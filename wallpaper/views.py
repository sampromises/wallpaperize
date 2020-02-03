import io
import logging
import os
import re
import sys

from PIL import Image
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from wallpaper.image.convert import create_wallpaper
from wallpaper.image.resolutions import Resolution
from wallpaper.image.resolutions import resolution
from wallpaper.image.util import get_final_filename
from wallpaper.image.util import get_image_format
from wallpaper.forms import InputForm
from wallpaper.image.util import parse_resolution
from wallpaper.models import Upload

log = logging.getLogger("app")


def redirect_wallpaper(request):
    log.info("Redirecting root to /wallpaper...")
    return redirect('/wallpaper')


def index(request):
    log.info("views.index called")
    template = loader.get_template('wallpaper/index.html')
    errors = []

    try:
        if request.method == 'POST' and request.FILES['image']:
            log.info("Starting to handle POST request with image...")
            image = Image.open(request.FILES['image'])
            filename = request.FILES['image'].name

            # TODO: Choose resolution
            try:
                width, height = parse_resolution(request.POST['resolution'])
                res = resolution(f"{width}x{height}", width, height)
                log.info(f"Resolution given:{res}")
            except:
                res = Resolution.DEFAULT
                log.info(f"Invalid resolution, using default:{Resolution.DEFAULT}")
                messages.error(request, f"Invalid resolution, using default: {res.width}x{res.height}")

            # TODO: Choose color, None will default to most common color
            color = None

            wallpaper = create_wallpaper(image, res, color)
            wallpaper_filename = get_final_filename(filename, res)
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
                "errors": errors,
                "form": InputForm(),
            }

            return HttpResponse(template.render(context, request))
    except Exception as e:
        log.exception(f"Exception caught while handling POST request:")
        context = {
            "errors": errors,
            "form": InputForm(),
        }
        messages.error(request, f"Something went wrong...")
        return HttpResponse(template.render(context, request))

    log.info(f"Responding to GET request...")
    context = {
        "form": InputForm()
    }
    return HttpResponse(template.render(context, request))
