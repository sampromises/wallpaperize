from django.db.models import DateTimeField
from django.db.models import FileField
from django.db.models import Model

from wallpaper_site.storage_backends import MediaStorage


class Upload(Model):
    file = FileField(storage=MediaStorage())
    uploaded_at = DateTimeField(auto_now_add=True)
