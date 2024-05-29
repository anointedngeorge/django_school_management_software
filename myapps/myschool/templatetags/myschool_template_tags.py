import importlib
import json
import os
from django import template
from django.template.loader import render_to_string
from django.contrib.auth.decorators import permission_required
from django.utils.html import format_html
from django.conf import settings
from decouple import config
from myschool.models.timetable import Timetable

from myschool.plugins.system_calendar import calenday_days

register = template.Library()

redirect_path = f"/{config('BASE_APP_NAME')}"



@register.simple_tag
def endswith_url(request=None, url='', checker=''):
    try:
        s = str(url).endswith(checker)
        return s
    except Exception as e:
        return str(e)


@register.filter
def bootstrap_form2(form):
    try:
        table_html = ''
        table_html += '<div class="row">'
        table_html += f'<div class="col-3">'
        table_html += f'<label>{form.label_tag()}</label>'
        table_html += f"{form}"
        table_html += '</div>'
        table_html += '</div>'
    except Exception as e:
        return format_html(f"<p>{e}</p>")


@register.filter
def bootstrap_form(form_list):
    try:
        table_html = ''
        containers = form_list.container
        # for 
        for index in range(0, len(containers)):
            container =  containers[index]
            table_html += '<div class="row">'
            for form_name in container:
                form = form_list[form_name]
                table_html += f'<div class="col-3">'
                table_html += f'<label>{form.label_tag()}</label>'
                table_html += f"{form}"
                table_html += '</div>'
            table_html += '</div>'

        return format_html(table_html)
    except Exception as e:
        return format_html(f"<p>{e}</p>")





@register.filter
def bootstrap_table(form_list):
    try:
        table_html = ''
        containers = form_list.container
        # 
        if len(containers) > 0:
            for index in range(0, len(containers)):
                container =  containers[index]
                student_name = form_list.students[index][0]
                student_code =  form_list.students[index][1]
                table_html += f'<tr id="tr_{index}">'
                table_html += f'<td>'
                table_html += f'<b>{form_list.students[index][0]}</b>'
                table_html += f'<input type="text" hidden name="student_{index}"  value="{student_name}" readonly />'
                table_html += f'<input type="text" hidden name="student_code_{index}"  value="{student_code}" readonly />'
                table_html += f'</td>'
                table_html += f'<td>'
                table_html += f"<b>{form_list.subject}</b>"
                table_html += f'<input type="text" hidden name="subject_{index}"  value="{form_list.subject}" readonly />'
                table_html += f'<input type="text" hidden name="subject_id_{index}"  value="{form_list.subject_id}" readonly />'
                table_html += '</td>'
                for form_name in container:
                    form = form_list[form_name]
                    table_html += f'<td>'
                    table_html += f'<label>{form.label_tag()}</label>'
                    table_html += f"{form}"
                    table_html += '</td>'

                table_html += f"<td><br /><br /><button type='button' data-counter='{index}' data-index='{student_code}' class='btn btn-sm btn-primary result_add_btn' id='result_add_btn_{index}'>Add</button></td>"
                table_html += '</tr>'
        else:
            table_html += '<tr>'
            for form_name in form_list:
                table_html += f'<td>'
                table_html += f'{form_name.label_tag()}'
                table_html += '</td>'
            table_html += '</tr>'

        return format_html(table_html)
    except Exception as e:
        return format_html(f"<p>{e}</p>")
    




@register.filter
def bootstrap_edit_table(form_list):
    try:
        table_html = ''
        containers = form_list.container
        # 
        if len(containers) > 0:
            for index in range(0, len(containers)):
                container =  containers[index]
                student_code =  form_list.students[index][1]
     
                table_html += f'<tr id="tr_{index}">'
                for form_name in container:
                    form = form_list[form_name]
                    table_html += f'<td>'
             
                    table_html += f'{form.label_tag()}'
                    table_html += f"{form}"
                    table_html += '</td>'
                table_html += f"<td><br /><br /><button type='button' data-counter='{index}' data-index='{student_code}' class='btn btn-sm btn-primary result_add_btn' id='result_add_btn_{index}'>Add</button></td>"
                table_html += '</tr>'
        else:
            table_html += '<tr>'
            for form_name in form_list:
                table_html += f'<td>'
                table_html += f'{form_name.label_tag()}'
                table_html += '</td>'
            table_html += '</tr>'

        return format_html(table_html)
    except Exception as e:
        return format_html(f"<span>No Result Found: {e}</span>")


@register.simple_tag
def network(name='', path = "../myapps/myschool/network_urls.json"):
    # /home/sharashell/DjangoProjects/learn_django_dashboard/myapps/myschool/network_urls.json

    if os.path.exists(path):
        with open(os.path.realpath(path), 'r') as file :
            data = json.load(file)
            if dict(data).__contains__(name):
                return dict(data).get(name)
            else:
                return f"{name} does not exist!"     
    else:
        return "..."
    


@register.simple_tag
def table_heading(columns='total,'):
    try:
        table = ""
        cols = [x for x in str(columns).split(",") if x != '']
        table += f"<th>#</th>"
        for x in cols:
            table += f"<th>{str(x).upper()}</th>"
        return format_html(table)
    except Exception as e:
        return f"{e}"


@register.simple_tag
def table_rows(data=[], columns=''):
    try:
        table = ""
        for index, dt in enumerate(data):
            indx = index + 1
            table += f"<tr>"
            cols = [x for x in str(columns).split(",") if x != '']
            table += f"<td>{indx}</td>"
            for x in cols:
                table += f"<td>{dt.get(x)}</td>"
            table += f"</tr>"
        return format_html(table)
    except Exception as e:
        return f"{e}"
    


@register.inclusion_tag("admin/graph/student_performance.html", takes_context=True)
def pandas_graph(context, data=[], columns="total", chart_type='bar'):
    """
        kind: This parameter specifies the type of plot to create. It can be one of the following values:

        'line': Line plot
        'bar': Bar plot
        'barh': Horizontal bar plot
        'hist': Histogram
        'box': Box plot
        'kde': Kernel Density Estimation plot
        'density': Same as 'kde'
        'area': Area plot
        'pie': Pie plot
        'scatter': Scatter plot
        In this case, chart_type is used as the type of plot to create.
    """
    supported_chart_types = ['hist', 'bar', 'area', 'line', 'barh', 'box']
    try:
        context = context
        import pandas as pd
        import matplotlib.pyplot as plt
        from io import BytesIO
        import base64

        if not str(chart_type) in supported_chart_types:
            context['error'] = True
            context['message'] = f"{str(chart_type).upper()} is not supported. Supported types: {supported_chart_types}"
            return context

        cols = str(columns).split(",")
        # Create a DataFrame from the data
        df = pd.DataFrame(data)
        # Convert relevant columns to numeric
        numeric_columns = cols
        df[numeric_columns] = df[numeric_columns].apply(pd.to_numeric)
  
        # Plotting
        plt.figure(figsize=(10, 6))
        df.plot(x='subject', y=cols, kind=chart_type)
 
        plt.title('Student Performance')
        plt.xlabel('Subject')
        plt.ylabel('Marks')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        # Save the plot to a BytesIO object
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        # Encode the plot image to base64
        graphic = base64.b64encode(image_png)
        graphic = graphic.decode('utf-8')
        graphic = f'data:image/png;base64,{graphic}'
        context['graphic'] = graphic
        context['error'] = False
        return context
     
    except Exception as e:
        return f"{e}"
    


@register.simple_tag
def grading(data:dict, code:str, divisor:int):
    try:
        import pandas as pd
        import numpy as np

        # Convert the dictionary into a pandas DataFrame
        df = pd.DataFrame.from_dict(data, orient='index')

        # Fill missing values with NaN
        df.fillna(np.nan, inplace=True)

        # Calculate the total score for each student, and divide to get the average of the total value
        df['Total'] = df.sum(axis=1) / divisor

        # Determine the positions based on the total score
        positions = df['Total'].rank(method='min', ascending=False).astype(int)

        # Map position numbers to ordinal numbers
        positions = positions.map(lambda x: f"{x}{'th' if 10 <= x % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(x % 10, 'th')}")

        # Create a dictionary with student IDs as keys and positions as values
        positions_dict = positions.to_dict()
        # check if code exist
        if positions_dict.__contains__(code):
            return positions_dict.get(code)
        else:
            return f"{code} provided does not exist!"
    except Exception as e:
        return f"{e}"


@register.simple_tag
def average(data:dict, code:str, divisor:int):
    try:
        if data.__contains__(code):
            av = sum(data.get(code))
            if (isinstance(av, int) and (isinstance(divisor, int))):
                return av / divisor
            else:
                return "..."
            
    except Exception as e:
        return f"{e}"
    

@register.inclusion_tag('admin/templateresponse/show_timetable.html', takes_context=True)
def getTimetable(context):
        try:
            context = context
            container = {}
            days = calenday_days()
            for day in days:
                f = day[0]
                obj = Timetable.objects.filter(days=f)
                ob =[x for x in obj]
                container.update({f: ob})

            context['durations'] = [x.time for x in Timetable.objects.all() ]
            context['datas'] = container
            # print(container)
            return context
        except Exception as e:
            return e
        
def getdata(obj:object, name=''):
    try:
        return obj.get(name)
    except Exception as e:
        print(e)