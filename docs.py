# {% load admin_custom_template_tags %}
# {% get_data 'appcore.models.SystemSettings' name='settingname' as setting %}


# {% if setting.context.slider_choice == 'slider' %}
#   {% include "mega/sliders/slider.html" %}
# {% elif setting.context.slider_choice == 'property' %}
# {% include "mega/sliders/property_slider.html" %}
# {% endif %}