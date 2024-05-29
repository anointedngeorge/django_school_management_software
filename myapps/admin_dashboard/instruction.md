**_ useful templatetags functions _**
load: {% load admin_custom_template_tags %}

show count
{% show_count object='appname.models.Modelname' %}

<!-- with parameters as kwargs for filtering -->

{% show_count object='appname.models.Modelname' id=1 date='2024-09-01' %}

**_ for change form url _**
{% url 'app_name:changeform' 'appname' 'Modelname' %}

<!-- example -->

{% url 'admin_dashboard:changelist' 'branches' 'Branch' %}
{% url 'admin_dashboard:changeform' 'branches' 'Branch' %}

**_ for updating _**

{% url 'app_name:updateform' 'appname' 'objectid' 'Modelname' %}

<!-- example -->

{% url 'seller_dashboard:updateform' 'branches' 2 'Branch' %}

**_ for deleting _**

{% url 'app_name:delete' 'appname' 'objectid' 'Modelname' %}

<!-- example -->

{% url 'seller_dashboard:delete' 'branches' 2 'Branch' %}
