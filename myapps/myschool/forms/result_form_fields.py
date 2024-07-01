RESULT_PERMANENT_FORM_FIELDS = [
    # top fields, must be included
    {'name':'student','readonly':False, 'classname':'fields', 'has_choices':False, 'value':"", 'choices':[], 'is_hidden':False },
    {'name':'student_code','readonly':False, 'classname':'fields', 'has_choices':False, 'value':"", 'choices':[], 'is_hidden':False },
    {'name':'subject','readonly':False, 'classname':'fields', 'has_choices':False, 'value':"", 'choices':[], 'is_hidden':False },
    {'name':'subject_id','readonly':False, 'classname':'fields', 'has_choices':False, 'value':"", 'choices':[], 'is_hidden':False },
    # top fields ends here
]



# this is the result fields to update
REPLACABLE_FIELDS = [
    
    {'name':'assignment','readonly':False, 'classname':'fields', 'has_choices':False, 'value':"", 'choices':[], 'is_hidden':False },
    {'name':'quiz1', 'readonly':False, 'classname':'fields', 'has_choices':False, 'value':"", 'choices':[], 'is_hidden':False },
    {'name':'quiz2', 'readonly':False, 'classname':'fields', 'has_choices':False, 'value':"", 'choices':[], 'is_hidden':False },
    {'name':'quiz3', 'readonly':False, 'classname':'fields', 'has_choices':False, 'value':"", 'choices':[], 'is_hidden':False },

]

MAIN_RESULT_FIELDS = REPLACABLE_FIELDS + [

    # irreplacable fields
    {'name':'exams', 'readonly':False, 'classname':'fields', 'has_choices':False, 'value':"", 'choices':[], 'is_hidden':False },
    # for grading purpose, not to be touched
    {'name':'total', 'readonly':True, 'classname':'total nonefields', 'has_choices':False, 'value':"", 'choices':[], 'is_hidden':False },
    {'name':'grade', 'readonly':True, 'classname':'grade nonefields', 'has_choices':False, 'value':"", 'choices':[
            ('A',' A'),
            ('B',' B'),
            ('C',' C'),
            ('E',' E'),
            ('F',' F'),
    ], 'is_hidden':False },
     {'name':'remarks', 'type':'text', 'readonly':True, 'classname':'remarks nonefields', 'has_choices':False, 'value':"", 'choices':[
            ('excellent','Excellent'),
            ('very_good',' Very Good'),
            ('good',' Good'),
            ('fair',' Fair'),
            ('poor',' Poor'),
    ], 'is_hidden':False },
]