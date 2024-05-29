import os
import json
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