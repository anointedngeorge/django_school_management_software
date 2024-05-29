from django import forms
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.forms import AuthenticationForm
from appcore.models import SystemSettings, SystemSettingLogos
from imagekit.forms import ProcessedImageField
from imagekit.processors import ResizeToFill

from admin_dashboard.plugins.widgets import load_directory_contents
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

loginForms = load_directory_contents(path='templates/admin_custom/login_pages')
dashboard_index = load_directory_contents(path='templates/admin_custom/dashboard')


class SettingsForm(forms.Form):
    title = forms.CharField(max_length=200, required=True)
    sidemenu_title = forms.CharField(max_length=200, required=True)
    address = forms.CharField(max_length=200, required=True)
    tel = forms.CharField(max_length=200, required=True)
    email = forms.CharField(max_length=200, required=True)
    top_text =  forms.CharField(max_length=100)
    short_description = forms.CharField(max_length=300)
    copyright = forms.CharField(max_length=300)
    result_fields = forms.CharField(max_length=300)
    show_result_graph = forms.ChoiceField(
        choices=[('True','Yes'), ('False','No')],
        initial='False'
    )
    login_form = forms.ChoiceField(
        choices=loginForms,
        initial='default'
    )

    dashboard_index = forms.ChoiceField(
        choices=dashboard_index,
        initial='default'
    )

    api_version = forms.CharField(max_length=300, required=True)
   
    def __init__(self, setting_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            settings =  SystemSettings.objects.all().filter(name=setting_name)
            # print(settings)
            if settings.exists():
                found_settings = settings.first().context
                for fieldname, field in self.fields.items():
                    # converted to valid json
                    val_name = found_settings.get(fieldname)
                    # 
                    if fieldname == "login_form":
                        field.initial = val_name
                    
                    if fieldname == "dashboard_index":
                        field.initial = val_name

                    if fieldname == "show_result_graph":
                        field.initial = val_name
                    # 
                    field.widget.attrs.update({'class': 'form-control form-control-lg', 'value':str(val_name)})
            else:
                for fieldname, field in self.fields.items():
                    field.widget.attrs.update({'class': 'form-control form-control-lg'})
        except Exception as e:
            import traceback
            # traceback.print_exc()
            return e
       


class TemplateSettingsForm(forms.Form):
    result_not_found = forms.CharField(max_length=200, required=True)
    login_title = forms.CharField(max_length=200, required=True)
    login_button = forms.CharField(max_length=200, required=True)
    login_button_color = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'type':'color'}))
    login_button_text_color = forms.CharField(max_length=200, required=True, widget=forms.TextInput(attrs={'type':'color'}))
    login_bottom = forms.CharField(max_length=200, required=True)

    def __init__(self, setting_name=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            settings =  SystemSettings.objects.all().filter(name=setting_name)
            # print(settings)
            if settings.exists():
                found_settings = settings.first().context
                for fieldname, field in self.fields.items():
                    # converted to valid json
                    val_name = found_settings.get(fieldname)
                    field.widget.attrs.update({'class': 'form-control form-control-lg', 'value':str(val_name)})
            else:
                for fieldname, field in self.fields.items():
                    field.widget.attrs.update({'class': 'form-control form-control-lg'})
        except Exception as e:
            import traceback
            # traceback.print_exc()
            return e
       




class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'autofocus': True}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control form-control-lg'})
        self.fields['password'].widget.attrs.update({'class': 'form-control form-control-lg'})





class SettingsLogosForm(forms.ModelForm):
    logo = ProcessedImageField(spec_id='staff_dashboard:systemsettinglogos:logo',
                                           processors=[ResizeToFill(100, 100)],
                                           format='png',
                                           options={'quality': 80})
    favicon = ProcessedImageField(spec_id='staff_dashboard:systemsettinglogos:favicon',
                                           processors=[ResizeToFill(70, 70)],
                                           format='png',
                                           options={'quality': 80})
    class Meta:
        model= SystemSettingLogos
        fields = "__all__"


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for x in self.fields:
            self.fields[x].widget.attrs.update({'class': 'form-control'})




