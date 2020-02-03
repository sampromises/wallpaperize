from typing import List

from django import forms

from wallpaper.image.resolutions import Resolution


class ListResolutionWidget(forms.TextInput):
    def __init__(self, res_list, *args, **kwargs):
        super(ListResolutionWidget, self).__init__(*args, **kwargs)
        self._name = "res-list"
        self._res_list = res_list  # type: List[Resolution]
        self.attrs.update({'list': self._name})
        self.attrs.update({'autocomplete': "off"})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(ListResolutionWidget, self).render(name, value, attrs=attrs)
        data_list = f'<datalist id="{self._name}">'
        for res in self._res_list:
            data_list += f'<option value="{res.name}">'
        data_list += '</datalist>'

        return text_html + data_list
