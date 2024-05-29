from myschool.models.school_module import (
            Sections,Classes,Term
        )
from myschool.plugins.session_generator import sessionGenerator

session = sessionGenerator(sessions=10)

def processors(request):
    try:     
        return {
            "classes":Classes.objects.all(),
            "sections":Sections.objects.all(),
            "terms":Term.objects.all(),
            "sessions":session
        }
    except:
        pass