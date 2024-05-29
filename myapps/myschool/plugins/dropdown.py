from django.utils.html import format_html
from django.urls import reverse_lazy

from plugins.url import (
    local_file_url_image,
    api_fetch_image
)


REPORT_LINK = '/admin/reports/get-reports'
def table_dropdown(title='choose', content=[{"name":"", "url":"","model":False}], adminsite='admin' ):
    
    links =  ""
    counter = 0
    try:
        for x in content:
            if not x.get('modal'):
                links += f'<a class="dropdown-item btn btn-sm" href="/{adminsite}/{x.get("url")}">{x.get("name")}</a>'
            else:
                links += f'<button id="modalbtn{counter}" type="button" class="btn btn-sm ml-3 modalPages" data-toggle="modal" data-target=".bs-example-modal-lg" data-url="/{adminsite}/{x.get("url")}" >{x.get("name")}</button>'
            counter = counter + 1

        ul = f'''<ul>
            <li class="dropdown">
            <a
                href="#"
                class="dropdown-toggle"
                data-toggle="dropdown"
                role="button"
                aria-expanded="false"
            >
                {title}
            </a>
            <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                {links}
            </div>
        </li>'''
        ul += "</ul>"

        return format_html(ul)
    except Exception as e:
        return "---"


def queryFormat(param={}):
    if len(param) > 0:
        str =  ""
        for x in param:
            str += f"{x}={param.get(x)}&"
            filtered =  str.rstrip('&')
        return filtered
    else:
        return ''

def dictDropdown(action=[], link='', status='', modelname='', code='', report_title='',  report_template_name='', is_report=False):
        """
        This is a dropdown menue
        """
        html = ""
        try:
            # get the status that match in the action object
            get_status =  None
            if not action.get(status) == None:
                get_status =  action.get(status)
            else:
                get_status = []
                
            html += "<div class='table table-responsive'>"
            html += "<table class='table table-sm table-condensed'>"
            html += "<tr>"
            query = ''
            for x in get_status:
                query = queryFormat(x.get('query')) if x.get('query') != None else ''
                if x.get('is_button'):
                    html += f"<td><button type='button' data-url='{x.get('href')}' value='{query}'>{str(x.get('name')).title()}</button></td>"
                else:
                    html += f"<td><a  href='{x.get('href')}?{query}'>{str(x.get('name')).title()}</a></td>"
            html += f"<td><a  href='{local_file_url_image(code)}?model={modelname}'>Upload File(s)</a></td>"
            html += f"<td><a  href='{api_fetch_image(code)}?model={modelname}' target='_blank'>Get Files</a></td>"
            if is_report:
                html += f"<td><a  href='{link}/{report_template_name}/{modelname}/?{query}'>{report_title.title()}</a></td>"

            html += "</tr>"
            html += "</table>"
            html += "</div>"

            return format_html(html)
        except:
            pass


def singleDropdown(action=[], modelname='', link='', code='', report_title='', report_template_name='task', is_report=False):
        try:
            html = ""
            # get the status that match in the action object
            html += "<div class='table table-responsive'>"
            html += "<table class='table table-sm table-condensed'>"
            html += "<tr>"
            query = ''
            for x in action:
                query = queryFormat(x.get('query')) if x.get('query') != None else ''
                if x.get('is_button'):
                    html += f"<td><button  data-url='{x.get('href')}' value='{query}'>{x.get('name')}</button></td>"
                else:
                    html += f"<td><a href='{x.get('href')}?{query}'>{x.get('name')}</a></td>"
            html += f"<td><a  href='{local_file_url_image(code)}?model={modelname}'>Upload File(s)</a></td>"
            html += f"<td><a  href='{api_fetch_image(code)}?model={modelname}' target='_blank'>Get Files</a></td>"
            
            if is_report:
                html += f"<td><a  href='{link}/{report_template_name}/{modelname}/?{query}'>{report_title.title()}</a></td>"
            
            html += "</tr>"
            html += "</table>"
            html += "</div>"

            return format_html(html)
        except:
            pass