from django import forms
class CoreAttrs:

    def list_display(self):
        return ["id"]
    
    def list_display_links(self):
        return []
    
    def list_editable(self):
        return []
    def list_filter(self):
        return ["id"]
    def list_max_show_all(self):
        return []
    def list_per_page(self):
        return []
    def list_select_related(self):
        return []
    def is_registered(self):
        return True
    
    def has_action(self):
        return False
    
    def has_dropdown_action(self):
        return False
    
    @classmethod
    def form_fields(cls):
        return []

    @classmethod
    def exclude(cls):
        return []

    @classmethod
    def form(cls):
        try:
            field_list = cls.form_fields()
            exclude_fields = cls.exclude()

            class LOADFORM(forms.ModelForm):
                class Meta:
                    model = cls
                    fields = field_list if field_list else '__all__'
                    if exclude_fields:
                        exclude = exclude_fields

                def __init__(self, *args, **kwargs):
                    super().__init__(*args, **kwargs)
                    for x in self.fields:
                        # name = self.fields[x].label
                        self.fields[x].widget.attrs.update({'class': 'form-control'})

            return LOADFORM
        except Exception as e:
            import traceback

    
    def extra_forms(self):
        try:
            return {}
        except:
            return {}
    
    def action(self):
        return []
    def dropdown_action(self):
        return []