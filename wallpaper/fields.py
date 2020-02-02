from typing import List

from django import forms

from wallpaper.backend.resolutions import Resolution


class ListResolutionWidget(forms.TextInput):
    def __init__(self, name, res_list, *args, **kwargs):
        super(ListResolutionWidget, self).__init__(*args, **kwargs)
        self._name = name
        self._res_list = res_list  # type: List[Resolution]
        self.attrs.update({'list': 'list__%s' % self._name})

    def render(self, name, value, attrs=None, renderer=None):
        text_html = super(ListResolutionWidget, self).render(name, value, attrs=attrs)
        data_list = f'<datalist id="list__{self._name}">'
        for res in self._res_list:
            data_list += f'<option value="{res.width}x{res.height}">{res.name}</option>'
        data_list += '</datalist>'

        return text_html + data_list
