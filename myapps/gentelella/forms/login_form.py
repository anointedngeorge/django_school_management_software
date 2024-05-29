
from django import forms
from django.forms import fields
from django.contrib.auth.forms import AuthenticationForm
from ..models import Plugins,Menus,SystemSettings

from decouple import config


class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['password'].widget.attrs.update({'class': 'form-control'})

    def confirm_login_allowed(self, user):
        pass


class PluginForm(forms.ModelForm):
    class Meta:
        model = Plugins
        fields = "__all__"



class MenusForm(forms.ModelForm):
    class Meta:
        model = Menus
        fields = "__all__"



# this will handle the settings
class SettingForm(forms.ModelForm):
    # 
    class Meta:
        model = SystemSettings
        fields = "__all__"



class PluginForm(forms.Form):
    file = forms.ImageField(required=True, widget=forms.FileInput(attrs={'accept':'.zip'}))
    plugin_type = forms.CharField(
                                  max_length=100, 
                                  required=True,
                                   widget=forms.Select(
                                    choices=[
                                            ('chart', 'Chart'),
                                            ('card', 'Card'),
                                            ('table', 'table'),
                                            ('history', 'History'),
                                        ]
        ))
