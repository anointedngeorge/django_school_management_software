import json
from django.shortcuts import redirect

from django.template.response import TemplateResponse
from django.http import HttpResponse, JsonResponse
from decouple import config
from myschool.plugins.system_calendar import calendar_workweeks
from myschool.plugins.result_widget import get_data

from myschool.models.attendance import Attendance, AttendanceRecords
from myschool.models.school_users import Students
from myschool.models.result import Results
from myschool.models.school_module import Sections, SubjectSelection
from myschool.forms.result_form import EditResultStudentForm, ResultStudentParameterForm
from urllib.parse import urlencode


BASE_DIR_NAME = 'admin_custom'


system_data = get_data(object="appcore.models.SystemSettings", name="settingname")


# this function is used to translate dict object to query format
# {'id':1,'name':'test'} = id=1&name=test
def convert_to_query(query):
    query_string = urlencode(query)
    return query_string



def getRelatedClassSections(request, id, query, context):
    try:
        context = context
        class_id =  query.get("class_id")
        section = Sections.objects.all().filter(classes_id=class_id)
        context['section']=section
        # 
        return TemplateResponse(
            request=request,
            template="admin/templateresponse/options.html",
            context=context,
            status=200,
        )
    except Exception as e:
        return str(e)



def annual_results(request, id, query, context):
    try:
        context = context
        context['query'] = query
        context['id'] = id
        return TemplateResponse(
            request=request,
            template="admin/templateresponse/annual_results.html",
            context=context,
            status=200,
        )
    except Exception as e:
        return str(e)




# this function is by javascript in the change_form in myschool app.
def result_load_student(request, id, query, context):
    try:
        context = context
        context['title'] = "Register Results"
        context['is_result_exist'] = False
        context['query'] = query
        # print(query)
        teacher_id = query.get('teacher_id')
        subject_id = query.get('subject_id')
        section_id = query.get('sections_id')
        classes_id = query.get('classes_id')
        term_id = query.get('term_id')
        session = query.get('session')
        query = {
            'subject_id':subject_id,
            'sections_id':section_id,
            'teacher_id':teacher_id, 
            'classes_id':classes_id,
            'term_id':term_id,
            'session':session,
            }
        query_url = convert_to_query(query=query)

        results = Results.objects.all()
        # this line checks whether result already exist, to force the user to use other options,
        # other than adding  a new result, to avoid duplicate data.
        if results.filter(**query).exists():
            context['is_result_exist'] = True
        selected_courses = SubjectSelection.objects.all().filter(**query).first()
        context['student_form'] = ResultStudentParameterForm(context=query)
        context['selected_courses'] = selected_courses
        context['query_url'] = query_url

        return TemplateResponse(
            request=request,
            template=f"{BASE_DIR_NAME}/templateresponse/admin_add_result.html",
            context=context,
            status=200,
        )
    except Exception as e:
        return HttpResponse(e)


    
def loadResultform(request, id, query, context):
    try:
        context = context
        # context['title'] = "Register Results"
        context['query'] = query
        # print(query)
        teacher_id = query.get('teacher_id')
        subject_id = query.get('subject_id')
        sections_id = query.get('sections_id')
        classes_id = query.get('classes_id')
        term_id = query.get('term_id')
        session = query.get('session')
        query = {
            'subject_id':subject_id,
            'sections_id':sections_id,
            'teacher_id':teacher_id, 
            'classes_id':classes_id,
            'term_id':term_id,
            'session':session,
            }
        results = Results.objects.all()

        if results.filter(**query).exists():
            
            return JsonResponse({"message":"Result already exist, please use the Edit button"})
        
        students = Students.objects.all().filter(classes_id=classes_id, sections_id=sections_id)
        # cross check if a student exists in the result sheet provide.
        # to avoid registering a student that does not exist at all.
        container = {}
        if students.exists():
            prepared_to_json = json.loads(request.body)

            for student in students:
                # filter to know students that are available in the class
                # second layer of security
                if prepared_to_json.__contains__(student.code):
                    container[student.code] = prepared_to_json.get(student.code) 

        results.create(**query, result=container)

        return JsonResponse({"message":"Successful"})
    except Exception as e:
        return JsonResponse({"message":e})






# editing results
def result_edit_student(request, id, query, context):
    try:
        context = context
        context['title'] = "Edit Results"
        context['is_result_exist'] = False
        context['query'] = query
        # print(query)
        teacher_id = query.get('teacher_id')
        subject_id = query.get('subject_id')
        section_id = query.get('sections_id')
        classes_id = query.get('classes_id')
        term_id = query.get('term_id')
        session = query.get('session')
        query = {
            'subject_id':subject_id,
            'sections_id':section_id,
            'teacher_id':teacher_id, 
            'classes_id':classes_id,
            'term_id':term_id,
            'session':session,
            }
        query_url = convert_to_query(query=query)

        results = Results.objects.all()
        # this line checks whether result already exist, to force the user to use other options,
        # other than adding  a new result, to avoid duplicate data.
        # if results.filter(**query).exists():
        #     context['is_result_exist'] = True

        rs = Results.objects.all().filter(**query)
        if rs.exists():
            rs =  rs.first()
            context['title'] = f"{rs.teacher} {rs.subject} {rs.term} {rs.session}"
            context['subject_title'] = f"{rs.subject}".capitalize()
            context['page_title'] = f"Edit result for - {rs.teacher} {rs.subject} {rs.term} {rs.session}"
            context['student_form'] = EditResultStudentForm(object_id=rs.id)
            context['selected_results'] = rs
            context['query_url'] = query_url

        return TemplateResponse(
            request=request,
            template=f"{BASE_DIR_NAME}/templateresponse/admin_edit_result.html",
            context=context,
            status=200,
        )
    except Exception as e:
        return str(e)


def updateResultform(request, id, query, context):
    try:
        context = context
        # context['title'] = "Register Results"
        context['query'] = query
        # print(query)
        teacher_id = query.get('teacher_id')
        subject_id = query.get('subject_id')
        section_id = query.get('sections_id')
        classes_id = query.get('classes_id')
        term_id = query.get('term_id')
        session = query.get('session')
        query = {
            'subject_id':subject_id,
            'sections_id':section_id,
            'teacher_id':teacher_id, 
            'classes_id':classes_id,
            'term_id':term_id,
            'session':session,
            }
        results = Results.objects.all()

        if results.filter(**query).exists():
            dt = results.filter(**query).first()
            prepared_to_json = json.loads(request.body)
            # update the result
            dt.result = prepared_to_json
            # and save the result
            dt.save()
        return JsonResponse({"message":"Result Updated Successfully..."})
    except Exception as e:
        return JsonResponse({"message":e})




def printresult(request, id, query, context):
    try:
   
        if request.method == "POST":
            student_container = []
            context = context
            context['title'] = "Print Results"
            context['query'] = query
            data = request.POST.dict()
            # remove csrf token from the post request
            data.pop("csrfmiddlewaretoken")
            container = []
            foundResults = Results.objects.all().filter(**data)
            students =  Students.objects.all()
       
            if foundResults.exists():
                STUDENT_CONTEXT = {}
                STUDENT_CONTEXT_AVERAGE = {}
                STUDENT_CONTEXT_TOTAL = {}
                classes_id = data.get('classes')
                sections_id = data.get('sections')
                foundStudents = students.filter(classes_id=classes_id, sections_id=sections_id)

                
                # REGISTER STUDENTS IN A CONTEXT TO AVOID DUPLICATE DATA
                for student in foundStudents:
                    STUDENT_CONTEXT[student.code] = {
                        "fullname":"", "student_code":"", "subject":"", "classes":"","position":"Ist",
                        "sections":"", "session":"", "term":"", "total":0,
                        "average":0, "data":[]
                    }
                    STUDENT_CONTEXT_AVERAGE[student.code] = []
                    STUDENT_CONTEXT_TOTAL[student.code] = []

                for index, foundResult in enumerate(foundResults):
                    
                    result = foundResult.result
                    subject =  foundResult.subject.name
                    classes = foundResult.classes.name
                    sections = foundResult.sections.name.name
                    session = foundResult.session
                    term = foundResult.term.name

                    # print(foundStudents, 'students')

                    # group the students result from different teachers, subjects
                    for student in foundStudents:
                        student_code = student.code
                       
                        if ((STUDENT_CONTEXT.__contains__(student_code)) and (result.get(student_code) != None)):
                            # total = 0
                            student_fullname = f"{student.first_name} {student.middle_name} {student.last_name}"
                            # school information
                            STUDENT_CONTEXT.get(student_code)["school_title"] = "St. Augustin Secondary School"
                            STUDENT_CONTEXT.get(student_code)["school_address"] = "24, ABC street, DEF Road, Enugu State"
                            STUDENT_CONTEXT.get(student_code)["school_phone"] = "9876543210"
                            STUDENT_CONTEXT.get(student_code)["school_email"] = "admin@saphss.com"


                            STUDENT_CONTEXT.get(student_code)["fullname"] = student_fullname
                            STUDENT_CONTEXT.get(student_code)["student_code"] = student_code
                            STUDENT_CONTEXT.get(student_code)["photo"] = student.photo.path if student.photo else ''
                            STUDENT_CONTEXT.get(student_code)["subject"] = subject
                            STUDENT_CONTEXT.get(student_code)["classes"] = classes
                            STUDENT_CONTEXT.get(student_code)["sections"] = sections
                            STUDENT_CONTEXT.get(student_code)["session"] = session
                            STUDENT_CONTEXT.get(student_code)["term"] = term
                            STUDENT_CONTEXT.get(student_code)["class_no"] = foundStudents.count()
                            total =  result.get(student_code).get('total')
                            STUDENT_CONTEXT.get(student_code)["total"] += int(total)
                            # update STUDENT_CONTEXT_AVERAGE
                            # total no of subjects / by the summation of each subject total = average
                            STUDENT_CONTEXT.get(student_code)["subject_total"] = foundResults.count()
                            STUDENT_CONTEXT_AVERAGE.get(student_code).append(int(total))
                            STUDENT_CONTEXT_TOTAL.get(student_code).append(int(total))
                            STUDENT_CONTEXT.get(student_code)["data"].append(result.get(student_code))
                
                
                FILTERED_STUDENT_CONTEXT_TOTAL = {x:y for x,y in STUDENT_CONTEXT_TOTAL.items() if len(y) > 0 }
                FILTERED_STUDENT_CONTEXT_AVERAGE = {x:y for x,y in STUDENT_CONTEXT_AVERAGE.items() if len(y) > 0 }

                for student in foundStudents:
                    student_code = student.code
                    # Push into an array using the student code to filter the result,
                    # so that it can be easily accessed.
                    student_container.append(STUDENT_CONTEXT.get(student_code))
            context['bulk_results'] = student_container
            context['bulk_positions'] = FILTERED_STUDENT_CONTEXT_TOTAL
            context['bulk_averages'] = FILTERED_STUDENT_CONTEXT_AVERAGE
            context['is_graph_shown'] = eval(system_data.get('show_result_graph', "False"))
            context['graph_fields'] = "total"
            # get the result fields from the settings model
            context['result_headings'] = system_data.get('result_fields', "student, total")
  

            return TemplateResponse(
                request=request,
                template="admin_custom/templateresponse/termly_results.html",
                context=context,
                status=200,
                
            )
        else:
            return redirect("admin_dashboard:index")
    except Exception as e:
        # print("Error: ",e)
        return HttpResponse({"message":e})
    




def take_attendance(request, id, query, context):
    try:
        context = context
        context['title'] = "Take Attendance"
        context['page_title'] = "Attendance Register"
        
        return TemplateResponse(
            request=request,
            template="admin/templateresponse/take_attendance.html",
            context=context,
            status=200,
        )
    except Exception as e:
        return JsonResponse({"message":e})


def selected_student_attendance(request, id, query, context):
    try:
        context = context
        context['title'] = "Selected Students"
        context['page_title'] = "Attendance Register"
        code = query.get('code')

        attendance = Attendance.objects.all().filter(code=code)

        if not attendance.exists():
                context['has_code']=False
                return TemplateResponse(request=request,template="admin/templateresponse/selected_student_attendance.html",
                context=context, status=200,
            )
        else:
            att = attendance.first()
            students = Students.objects.filter(
                classes_id=att.classes_id,
                sections_id=att.sections.id
            )
            context['has_code']=True
            context['attendance'] = att
            context['calendar'] = calendar_workweeks()
            context['students'] = students

            return TemplateResponse(
                request=request,
                template="admin/templateresponse/selected_student_attendance.html",
                context=context,
                status=200,
            )
    except Exception as e:
        return JsonResponse({"message":e})
    


# for registering an attendance
def register_attendance(request, id, query, context):
    try:
        context = context
        bn = json.loads(request.body)
        fm = bn
        fm.pop("morning")
        fm.pop("afternoon")
        # print(bn)
        attend = AttendanceRecords.objects.all()
        if attend.filter(**fm).exists():
            attend.filter(**fm).update(**bn)
            c = attend.filter(**fm).first()
            return JsonResponse({"message":f"Attedance Updated {c.student}"})
        else:
            c =attend.create(**bn)
            return JsonResponse({"message":f"Attendance Created for {c.student}"})
    except Exception as e:
        return JsonResponse({"message":e})
    
def printidcard(request, id, query, context):
    try:
        
        return TemplateResponse(
                request=request,
                template="admin/templateresponse/printidcard.html",
                context=context,
                status=200,
                
            )
    except Exception as e:
        pass