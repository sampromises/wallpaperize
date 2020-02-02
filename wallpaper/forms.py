import logging

from django import forms
from django.forms import Form
from django.forms import ImageField

from wallpaper.backend.resolutions import Resolution
from wallpaper.fields import ListResolutionWidget

log = logging.getLogger("app")


class InputForm(Form):
    image = ImageField()
    resolution = forms.CharField(
        required=True,
        help_text="Choose your device from the dropdown or enter your own resolution (e.g. 1920x1080)"
    )

    def __init__(self, *args, **kwargs):
        log.info(f"List of resolutions:\n{[res for res in Resolution]}")
        _res_list = kwargs.pop('res_list', Resolution)
        super(InputForm, self).__init__(*args, **kwargs)

        # the "name" parameter will allow you to use the same widget more than once in the same
        # form, not setting this parameter differently will cuse all inputs display the
        # same list.
        self.fields['resolution'].widget = ListResolutionWidget(res_list=_res_list, name='res-list')
