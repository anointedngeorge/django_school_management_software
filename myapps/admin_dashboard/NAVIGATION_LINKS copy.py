import uuid
from django.urls import reverse


def link(appname='admin_dashboard',modelname='changelist', **kwargs):
    try:
        concat = f"{appname}:{modelname}"
        url = reverse(concat, kwargs=kwargs)
        return url
    except Exception as e:
        return str(e)


NAVIGATION_LINKS = [
    # start
    {   
        "groupname":"Utilities",
        "title":"Utitities",  
        "icon":"icon-layers menu-icon",
        "href":link(appname="myschool", modelname='Sections'),
        "has_dropdown":True, 
        "children":[
                    {"title":"Classes", "href":link(appname="myschool", modelname='Classes')},
                    {"title":"Create All Sections", "href":link(appname="myschool", modelname='SectionsNames')},
                    {"title":"Sections", "href":link(appname="myschool", modelname='Sections')}
                ],
    },


     {   
        "groupname":"Results",
        "title":"Results",  
        "icon":"icon-layers menu-icon",
        "href":link('admin_dashboard','resultprinting'),
        "has_dropdown":True, 
        "children":[
                    {"title":"Result Printing", "href":link('admin_dashboard','resultprinting')},
                ],
    },


    {   
        "groupname":"Teacher's Section",
        "title":"Teachers",  
        "icon":"icon-layers menu-icon",
        "href":link(appname="myschool", modelname='Teachers'),
        "has_dropdown":True, 
        "children":[
                    {"title":"List Teachers", "href":link(appname="myschool", modelname='Teachers')},
                    {"title":"Assign Subjects", "href":link(appname="myschool", modelname='SubjectSelection')},
                ],
    },


    {   
        "groupname":"Student's Section",
        "title":"Students",  
        "icon":"icon-layers menu-icon",
        "href":link(appname="myschool", modelname='Students'),
        "has_dropdown":False, 
        "children":[
                    {"title":"Sections", "href":link(appname="myschool", modelname='Sections')}
                ],
    },

    {   
        "groupname":"Settings Section",
        "title":"Settings",  
        "icon":"icon-layers menu-icon",
        "href":link('admin_dashboard', 'settings'),
        "has_dropdown":True, 
        "children":[
                    {"title":"General Settings", "href":link(appname='admin_dashboard', modelname='settings', name='settingname'),},
                    {"title":"Template Settings", "href":link(appname='admin_dashboard', modelname='settings', name='templatetext'),},
                ],
    },
      
      
# end
]


