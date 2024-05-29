from django import forms
from django.forms import TextInput
from decouple import config

from gentelella.plugins.custom_plugins import load_settings


theme_settings = load_settings(path=config("SETTINGS_JSON_PATH"))


class SettingsForm(forms.Form):
    
    def __init__(self, context={}, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)

        for x in theme_settings:
            self.fields[x] = forms.CharField(
                initial=theme_settings.get(x),
                widget=TextInput(attrs={'class':'form-control form-control-sm'})
            )