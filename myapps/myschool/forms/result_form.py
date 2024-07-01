from django import forms
# from django.contrib.postgres.forms.jsonb import JSONField
import json
from myschool.forms.result_form_fields import *
from myschool.plugins.session_generator import sessionGenerator
from myschool.models.school_module import Classes, Sections, SubjectSelection, Term
from myschool.models.school_users import Students
from myschool.models.result import Results
from django.forms.widgets import TextInput
import importlib



class ResultForm(forms.ModelForm):

    class Meta:
        model = Results
        # fields = "__all__"
        fields = [
                    'teacher',
                    'classes','sections','term','subject','session'
                  ]
        
# start of add result form field

complex_fields_for_add_result = RESULT_PERMANENT_FORM_FIELDS + MAIN_RESULT_FIELDS
complex_fields_for_add_result_filter = []

# for editing
complex_fields_for_edit_result_filter = []

FORM_LABEL_HEADS = [x.get('name') for x in MAIN_RESULT_FIELDS]
# exclude form fields you do not want to display
# server for both edit and add form
FORM_LABEL_HEADS_FOR_RESULT_EXCLUDE = ['subject_id']

# ...........................................
FORM_LABEL_HEADS_FOR_RESULT = []
# perform form field exclusion
for x in complex_fields_for_add_result:
    if x.get('name') not in FORM_LABEL_HEADS_FOR_RESULT_EXCLUDE:
        FORM_LABEL_HEADS_FOR_RESULT.append(x.get('name'))
        complex_fields_for_add_result_filter.append(x)


# ..........................................................................
class ResultStudentParameterForm(forms.Form):
    # creating a dynamic django forms
    def __init__(self, context={}, *args, **kwargs):
        super(ResultStudentParameterForm, self).__init__(*args, **kwargs)
        self.container = []
        self.students = []
        self.subject = "None"
        self.exclude = tuple(FORM_LABEL_HEADS_FOR_RESULT_EXCLUDE)
        self.teacher_id = context.get('teacher_id')
        self.subject_id = context.get('subject_id')
        self.section_id = context.get('sections_id')
        self.classes_id = context.get('classes_id')
        self.session = context.get('session')
        self.term_id = context.get('term_id')
        
        # set the form head
        self.label_heads = FORM_LABEL_HEADS_FOR_RESULT
        # update the complex field
        query = {
            'subject_id':self.subject_id,
            'sections_id':self.section_id,
            'teacher_id':self.teacher_id, 
            'classes_id':self.classes_id,
            'term_id':self.term_id,
            'session':self.session,
            }
        # select subject
        selected_courses = SubjectSelection.objects.all().filter(**query)
        # check if subject exist
        if selected_courses.exists():
            found_selected_courses = selected_courses.first()
            students = Students.objects.all().filter(
                sections_id=found_selected_courses.sections.id, 
                classes_id=found_selected_courses.classes.id
            )
            self.subject = found_selected_courses.subject
            self.subject_id = found_selected_courses.subject.id
            # 
            if students.exists():
                for index in range(0, len(students)):
                    foundStudent =  students[index]
                    name = f"{foundStudent.first_name} {foundStudent.last_name}"
                    # fetch the students registration code, and store it as a tuple
                    self.students.append((name, foundStudent.students.code))
                    # n is used to hold the forms field names, and order it will printing it out.
                    # [form_0,form_1 ...]
                    # [form_1, form_1 ...]
                    n = []
                    # iterate on the complex fields or result fields
                    
                    for x in range(0, len(complex_fields_for_add_result_filter)):
                        
                        data = complex_fields_for_add_result_filter[x]
                       
                        classname = data.get("classname")
                        readonly = data.get("readonly")
                        hidden = data.get("is_hidden", False)
                        # convert all names in data to have indexes, so the form can create properly
                        key = f"{data.get('name')}_{index}"

                        n.append(key)
                        # student the extra fields

                        self.fields[f"student_{index}"] = forms.CharField(
                                    label=f"student_{index}",
                                    widget=TextInput(
                                        attrs={
                                                'class':f'form_children_readonly result_{index}', 
                                                'readonly':True,
                                                'value':f"{foundStudent.first_name} {foundStudent.last_name}"
                                            }
                                    )
                                )

                        self.fields[f"subject_{index}"] = forms.CharField(
                                    label=f"student_{index}",
                                    widget=TextInput(
                                        attrs={
                                                'class':f'form_children_readonly result_{index}', 
                                                'readonly':True,
                                                'value':self.subject
                                            }
                                    )
                                )
                        self.fields[f"subject_id_{index}"] = forms.CharField(
                                    label=f"subject_id_{index}",
                                    widget=TextInput(
                                        attrs={
                                                'class':f'form_children_readonly', 
                                                'readonly':True,
                                                'value':self.subject_id
                                            }
                                    )
                                )
                        self.fields[f"student_code_{index}"] = forms.CharField(
                                    label=f"student_code_{index}",
                                    widget=TextInput(
                                        attrs={
                                                'class':f'form_children_readonly result_{index}', 
                                                'readonly':True,
                                                'value':foundStudent.code
                                            }
                                    )
                                )
                        
                        if data.get('has_choices'):
                            self.fields[key] = forms.ChoiceField(choices=data.get("choices"),
                                    widget=forms.Select(attrs={'class':f'form-children {classname} result_{index}', 'readonly':readonly}))
                        else:
                            self.fields[key] = forms.CharField(
                                    label=f"{key}",
                                    widget=TextInput(
                                    attrs={
                                            'class':f'form-children {classname} result_{index}', 
                                            'readonly':readonly,
                                            'hidden':hidden
                                        }
                                    )
                                )
                    
                    self.container.append(n)
                    # print(self.container)
                    
            else:
                self.fields['no_student_found'] = forms.CharField(
                                    label="No Student(s) found!",
                                    widget=TextInput(
                                        attrs={
                                            'class':f'form-control form-control-sm',
                                            'readonly':True,
                                        }
                                    )
                                )
        else:
            self.fields['no_student_found'] = forms.CharField(
                                    label="This teacher does not have an class registered yet.",
                                    widget=TextInput(
                                        attrs={
                                            'class':f'form-control form-control-sm',
                                            'readonly':True,
                                        }
                                    )
                                )
      

       
def foundUserForm(self, fields, index, foundResult, n):
    container = []

    for field in fields:
        nn = field.get("name")
        key = f"{nn}_{index}"
        initial_val = field.get('value')
        initial_data = initial_val if initial_val else foundResult.get(nn)
        classname = field.get("classname")
        readonly = field.get("readonly")
        is_hidden = field.get("is_hidden")
        show_label = field.get("show_label", True)
        # print(key)
        n.append(key)
        
        if field.get('has_choices'):
                self.fields[key] = forms.ChoiceField(
                initial=f"{initial_data}",
                choices=field.get("choices"),
                widget=forms.Select(attrs={
                        'class':f'form-children {classname} result_{index}',
                        'readonly':readonly,
                        'title':f"{initial_data}",
                        'hidden':is_hidden,
                        'show_label':show_label,
                    })
                )
        else:
            self.fields[key] = forms.CharField(
                    label=f"{key}",
                    initial=f"{initial_data}",
                    
                    widget=TextInput(
                        attrs={
                            'class':f'form-children {classname} result_{index}', 
                            'readonly':readonly,
                            'title':f"{initial_data}",
                            'hidden':is_hidden,
                            'show_label':show_label,
                        }
                    )
                )


def notfoundUserForm(self, fields, index, n):
    for field in fields:
        nn = field.get("name")
        key = f"{nn}_{index}"
        classname = field.get("classname")
        readonly = field.get("readonly")
        is_hidden = field.get("is_hidden")
        n.append(key)
        initial_data = field.get('value')
        if field.get('has_choices'):
                self.fields[key] = forms.ChoiceField(
                choices=field.get("choices"),
                initial=initial_data,
                widget=forms.Select(attrs={
                        'class':f'form-children {classname}', 
                        'readonly':readonly,
                        'title':f"{initial_data}",
                        'hidden':is_hidden,
                    })
                )
        else:
            self.fields[key] = forms.CharField(
                    label=f"{key}",
                    initial=initial_data,
                    widget=TextInput(
                        attrs={
                            'class':f'form-children {classname}', 
                            'readonly':readonly,
                            'title':f"{initial_data}",
                            'hidden':is_hidden,
                        }
                    )
                )


class EditResultStudentForm(forms.Form):
    # creating a dynamic django forms
    def __init__(self, object_id=None, *args, **kwargs):
        try:
            super(EditResultStudentForm, self).__init__(*args, **kwargs)
            result2 =  Results.objects.all().filter(id=object_id)
           
            result =  result2.first()
            sections_id = result.sections.id
            classes_id = result.classes.id
            self.exclude = ()
            selected_students = Students.objects.all().filter(classes_id=classes_id, sections_id=sections_id)
            self.container = []
            self.students = []
            get_results = result.result
            head_fields = ['student','student_code','subject','subject_id'] + FORM_LABEL_HEADS
            self.label_heads = [x for x in head_fields if x not in FORM_LABEL_HEADS_FOR_RESULT_EXCLUDE]
            
            if result2.exists():
                # order by students
                for index, stud in enumerate(selected_students):
                    n = []
                    fields2  =  [
                                {'name':'student','readonly':True, 'classname':'form_children_readonly', 'has_choices':False, 'value':f"{stud.first_name} {stud.last_name}", 'choices':[], 'is_hidden':False, 'show_label':True},
                                {'name':'student_code','readonly':True, 'classname':'form_children_readonly', 'has_choices':False, 'value':f"{stud.code}", 'choices':[], 'is_hidden':False, 'show_label':False},
                                {'name':'subject','readonly':True, 'classname':'form_children_readonly', 'has_choices':False, 'value':f"{result.subject.name}", 'choices':[], 'is_hidden':False, 'show_label':False},
                                {'name':'subject_id','readonly':True, 'classname':'form_children_readonly', 'has_choices':False, 'value':f"{result.subject.id}", 'choices':[], 'is_hidden':False, 'show_label':False},
                            ] + MAIN_RESULT_FIELDS
                    
                    # perform a field switch off.
                    # remove field if it is present in exclude function
                    fields = [x for x in fields2 if x.get('name') not in FORM_LABEL_HEADS_FOR_RESULT_EXCLUDE]
                   
                    # append the student object and student code
                    self.students.append((stud, stud.code))

                    foundResult = get_results.get(stud.code)
                    # print(foundResult)
                    if get_results.__contains__(stud.code):
                        foundUserForm(self=self, fields=fields, index=index, foundResult=foundResult, n=n)
                    else:
                        notfoundUserForm(
                            self=self,
                            fields=fields, 
                            index=index, 
                            n=n
                        )
                    self.container.append(n)
                # else:
                #     self.fields['no_student_found'] = forms.CharField(
                #         label="This teacher does not have an class registered yet.",
                #         widget=TextInput(
                #             attrs={
                #                 'class':f'form-control form-control-sm',
                #                 'readonly':True,
                #             }
                #         )
                #     )
        except Exception as e:
            pass
        
      



# print(class_objects)
class PrintResultForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(PrintResultForm, self).__init__(*args, **kwargs)
        class_objects = [(None, "Choose")]+[(x.id, x.name) for x in Classes.objects.all()]
        term_objects = [(None, "Choose")]+[(x.id, x.name) for x in Term.objects.all()]
        self.fields['classes'] = forms.ChoiceField(choices=class_objects, required=True)
        self.fields['sections'] = forms.ChoiceField(choices=[], required=True)
        self.fields['session'] = forms.ChoiceField(choices=sessionGenerator)
        self.fields['term'] = forms.ChoiceField(choices=term_objects, required=True)
        # self.fields['type'] = forms.ChoiceField(choices=[('term','Termly'), ('annual','Annual')] )

        for x in self.fields:
            self.fields[x].widget.attrs.update({'class': 'form-control'})

        
        