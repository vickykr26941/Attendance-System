from email import message
import json
from lib2to3.pytree import Base
import os
import sys
from datetime import datetime
from unittest import result
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from requests import session
from Attendance_System_App.models import Teachers, LeaveReportTeachers, LeaveReportStudents, FeedBackTeachers, Students, \
    Attendance, AttendanceReport, Subjects, SessionYearModel, CustomUser

from Attendance_System_App.models import Courses, StudentResult

from subprocess import run, PIPE

import pandas as pd
from tabulate import tabulate
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CUR_DIR = os.path.abspath(os.path.dirname(__file__))   # get current directory



def teacher_home(request):
    # For Fetch All Student Under Teacher
    subjects = Subjects.objects.filter(teacher_id=request.user.id)
    course_id_list = []
    for subject in subjects:
        course = Courses.objects.get(id=subject.course_id.id)
        course_id_list.append(course.id)

    final_course = []
    # removing Duplicate Course ID
    for course_id in course_id_list:
        if course_id not in final_course:
            final_course.append(course_id)

    students_count = Students.objects.filter(course_id__in=final_course).count()

    # Fetch All Attendance Count
    attendance_count = Attendance.objects.filter(subject_id__in=subjects).count()

    # Fetch All Approve Leave
    teacher = Teachers.objects.get(admin=request.user.id)
    leave_count = LeaveReportTeachers.objects.filter(teacher_id=teacher.id, leave_status=1).count()
    subject_count = subjects.count()

    # Fetch Attendance Data by Subject
    subject_list = []
    attendance_list = []
    for subject in subjects:
        attendance_count1 = Attendance.objects.filter(subject_id=subject.id).count()
        subject_list.append(subject.subject_name)
        attendance_list.append(attendance_count1)

    students_attendance = Students.objects.filter(course_id__in=final_course)
    student_list = []
    student_list_attendance_present = []
    student_list_attendance_absent = []
    for student in students_attendance:
        attendance_present_count = AttendanceReport.objects.filter(status=True, student_id=student.id).count()
        attendance_absent_count = AttendanceReport.objects.filter(status=False, student_id=student.id).count()
        student_list.append(student.admin.first_name)
        student_list_attendance_present.append(attendance_present_count)
        student_list_attendance_absent.append(attendance_absent_count)

    return render(request, "teacher_template/teacher_home_template.html",
                  {"students_count": students_count, "attendance_count": attendance_count, "leave_count": leave_count,
                   "subject_count": subject_count, "subject_list": subject_list, "attendance_list": attendance_list,
                   "student_list": student_list, "present_list": student_list_attendance_present,
                   "absent_list": student_list_attendance_absent})


def teacher_take_attendance(request):
    subjects = Subjects.objects.filter(teacher_id=request.user.id)
    session_years = SessionYearModel.object.all()
    return render(request, "teacher_template/teacher_take_attendance.html",
                  {"subjects": subjects, "session_years": session_years})


def teacher_take_attendance_face(request):
    subjects = Subjects.objects.filter(teacher_id=request.user.id)
    session_years = SessionYearModel.object.all()
    return render(request, "teacher_template/teacher_take_attendance_face.html",
                  {"subjects": subjects, "session_years": session_years})


@csrf_exempt
def get_students(request):
    subject_id = request.POST.get("subject")
    session_year = request.POST.get("session_year")

    subject = Subjects.objects.get(id=subject_id)
    session_model = SessionYearModel.object.get(id=session_year)
    students = Students.objects.filter(course_id=subject.course_id, session_year_id=session_model)
    list_data = []

    for student in students:
        data_small = {"id": student.admin.id, "name": student.admin.first_name + " " + student.admin.last_name}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def save_attendance_data(request):
    student_ids = request.POST.get("student_ids")
    subject_id = request.POST.get("subject_id")
    attendance_date = request.POST.get("attendance_date")
    session_year_id = request.POST.get("session_year_id")

    subject_model = Subjects.objects.get(id=subject_id)
    session_model = SessionYearModel.object.get(id=session_year_id)
    json_sstudent = json.loads(student_ids)
    # print(data[0]['id'])

    try:
        attendance = Attendance(subject_id=subject_model, attendance_date=attendance_date,
                                session_year_id=session_model)
        attendance.save()

        for stud in json_sstudent:
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport(student_id=student, attendance_id=attendance, status=stud['status'])
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


def teacher_update_attendance(request):
    subjects = Subjects.objects.filter(teacher_id=request.user.id)
    session_years = SessionYearModel.object.all()
    return render(request, "teacher_template/teacher_update_attendance.html",
                  {"subjects": subjects, "session_years": session_years})


@csrf_exempt
def get_attendance_dates(request):
    subject = request.POST.get("subject")
    session_year_id = request.POST.get("session_year_id")
    subject_obj = Subjects.objects.get(id=subject)
    session_year_obj = SessionYearModel.object.get(id=session_year_id)
    attendance = Attendance.objects.filter(subject_id=subject_obj, session_year_id=session_year_obj)
    attendance_obj = []
    for attendance_single in attendance:
        data = {"id": attendance_single.id, "attendance_date": str(attendance_single.attendance_date),
                "session_year_id": attendance_single.session_year_id.id}
        attendance_obj.append(data)

    return JsonResponse(json.dumps(attendance_obj), safe=False)


@csrf_exempt
def get_attendance_student(request):
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    list_data = []

    for student in attendance_data:
        data_small = {"id": student.student_id.admin.id,
                      "name": student.student_id.admin.first_name + " " + student.student_id.admin.last_name,
                      "status": student.status}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@csrf_exempt
def save_update_attendance_data(request):
    student_ids = request.POST.get("student_ids")
    attendance_date = request.POST.get("attendance_date")
    attendance = Attendance.objects.get(id=attendance_date)

    json_sstudent = json.loads(student_ids)

    try:
        for stud in json_sstudent:
            student = Students.objects.get(admin=stud['id'])
            attendance_report = AttendanceReport.objects.get(student_id=student, attendance_id=attendance)
            attendance_report.status = stud['status']
            attendance_report.save()
        return HttpResponse("OK")
    except:
        return HttpResponse("ERR")


def teacher_apply_leave(request):
    teacher_obj = Teachers.objects.get(admin=request.user.id)
    leave_data = LeaveReportTeachers.objects.filter(teacher_id=teacher_obj)
    return render(request, "teacher_template/teacher_apply_leave.html", {"leave_data": leave_data})


def teacher_apply_leave_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("teacher_apply_leave"))
    else:
        leave_date = request.POST.get("leave_date")
        leave_msg = request.POST.get("leave_msg")

        teacher_obj = Teachers.objects.get(admin=request.user.id)
        try:
            leave_report = LeaveReportTeachers(teacher_id=teacher_obj, leave_date=leave_date, leave_message=leave_msg,
                                               leave_status=0)
            leave_report.save()
            messages.success(request, "Successfully Applied for Leave")
            return HttpResponseRedirect(reverse("teacher_apply_leave"))
        except:
            messages.error(request, "Failed To Apply for Leave")
            return HttpResponseRedirect(reverse("teacher_apply_leave"))


def teacher_feedback(request):
    teacher_id = Teachers.objects.get(admin=request.user.id)
    feedback_data = FeedBackTeachers.objects.filter(teacher_id=teacher_id)
    return render(request, "teacher_template/teacher_feedback.html", {"feedback_data": feedback_data})


def teacher_feedback_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("teacher_feedback_save"))
    else:
        feedback_msg = request.POST.get("feedback_msg")

        teacher_obj = Teachers.objects.get(admin=request.user.id)
        try:
            feedback = FeedBackTeachers(teacher_id=teacher_obj, feedback=feedback_msg, feedback_reply="")
            feedback.save()
            messages.success(request, "Successfully Sent Feedback")
            return HttpResponseRedirect(reverse("teacher_feedback"))
        except:
            messages.error(request, "Failed To Send Feedback")
            return HttpResponseRedirect(reverse("teacher_feedback"))

# leave
def student_leave_view1(request):
    leaves = LeaveReportStudents.objects.all()
    return render(request, "teacher_template/student_leave_view.html", {"leaves": leaves})


def student_approve_leave(request, leave_id):
    leave = LeaveReportStudents.objects.get(id=leave_id)
    leave.leave_status = 1
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view1"))


def student_disapprove_leave(request, leave_id):
    leave = LeaveReportStudents.objects.get(id=leave_id)
    leave.leave_status = 2
    leave.save()
    return HttpResponseRedirect(reverse("student_leave_view1"))


def teacher_profile(request):
    user = CustomUser.objects.get(id=request.user.id)
    teacher = Teachers.objects.get(admin=user)
    return render(request, "teacher_template/teacher_profile.html", {"user": user, "teacher": teacher})


def teacher_profile_save(request):
    if request.method != "POST":
        return HttpResponseRedirect(reverse("teacher_profile"))
    else:
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        address = request.POST.get("address")
        password = request.POST.get("password")
        try:
            customuser = CustomUser.objects.get(id=request.user.id)
            customuser.first_name = first_name
            customuser.last_name = last_name
            if password != None and password != "":
                customuser.set_password(password)
            customuser.save()

            teacher = Teachers.objects.get(admin=customuser.id)
            teacher.address = address
            teacher.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("teacher_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("teacher_profile"))


def teacher_add_result(request):
    subjects = Subjects.objects.filter(teacher_id=request.user.id)
    session_years = SessionYearModel.object.all()
    return render(request, "teacher_template/teacher_add_result.html",
                  {"subjects": subjects, "session_years": session_years})


def save_student_result(request):
    if request.method != 'POST':
        return HttpResponseRedirect('teacher_add_result')
    # student_admin_id = request.POST.get('student_list')
    # --------------- bulk update of student result ----------------------
    # # print(request.POST.get('student_list'))
    subject_id = request.POST.get('subject')
    student_ids_list = request.POST.getlist('student_list')
    student_name_list = request.POST.getlist('student_name_list')
    student_assignment_marks_list = request.POST.getlist('assignment_marks_list')
    student_exam_marks_list = request.POST.getlist('exam_marks_list')

    # print(subject_id)
    # print(student_ids_list)
    # print(student_name_list)
    # print(student_assignment_marks_list)
    # print(student_exam_marks_list)
    
    ok = True
    for i in range(len(student_ids_list)):
        id = student_ids_list[i]
        assignment_marks = student_assignment_marks_list[i]
        exam_marks = student_exam_marks_list[i]
        student_subject_id = subject_id
        if exam_marks == '' or assignment_marks == '':
            continue
        student_obj = Students.objects.get(admin=id)
        subject_obj = Subjects.objects.get(id = student_subject_id)
        try:
            check_exist = StudentResult.objects.filter(subject_id=subject_obj, student_id=student_obj).exists()
            if check_exist:
                result = StudentResult.objects.get(subject_id=subject_obj, student_id=student_obj)
                result.subject_assignment_marks = assignment_marks
                result.subject_exam_marks = exam_marks
                result.save()
            else:
                result = StudentResult(student_id=student_obj, subject_id=subject_obj, subject_exam_marks=exam_marks,
                                   subject_assignment_marks=assignment_marks)
                result.save()
        except:
            ok = False
            break
    if ok:
        messages.success(request, "Successfully Added Result")
        return HttpResponseRedirect(reverse("teacher_add_result"))
    else:
        messages.error(request, "Failed to Add Result")
    return HttpResponseRedirect(reverse("teacher_add_result"))


    # ------------------- single student data update------------------------
    # assignment_marks = request.POST.get('assignment_marks')
    # exam_marks = request.POST.get('exam_marks')
    # subject_id = request.POST.get('subject')

    # student_obj = Students.objects.get(admin=student_admin_id)
    # subject_obj = Subjects.objects.get(id=subject_id)

    # try:
    #     check_exist = StudentResult.objects.filter(subject_id=subject_obj, student_id=student_obj).exists()
    #     if check_exist:
    #         result = StudentResult.objects.get(subject_id=subject_obj, student_id=student_obj)
    #         result.subject_assignment_marks = assignment_marks
    #         result.subject_exam_marks = exam_marks
    #         result.save()
    #         messages.success(request, "Successfully Updated Result")
    #         return HttpResponseRedirect(reverse("teacher_add_result"))
    #     else:
    #         result = StudentResult(student_id=student_obj, subject_id=subject_obj, subject_exam_marks=exam_marks,
    #                                subject_assignment_marks=assignment_marks)
    #         result.save()
    #         messages.success(request, "Successfully Added Result")
    #         return HttpResponseRedirect(reverse("teacher_add_result"))
    # except:
    #     messages.error(request, "Failed to Add Result")
    # return HttpResponseRedirect(reverse("teacher_add_result"))



@csrf_exempt
def fetch_result_student(request):
    subject_id = request.POST.get('subject_id')
    student_id = request.POST.get('student_id')
    student_obj = Students.objects.get(admin=student_id)
    result = StudentResult.objects.filter(student_id=student_obj.id, subject_id=subject_id).exists()
    if result:
        result = StudentResult.objects.get(student_id=student_obj.id, subject_id=subject_id)
        result_data = {"exam_marks": result.subject_exam_marks, "assign_marks": result.subject_assignment_marks}
        return HttpResponse(json.dumps(result_data))
    else:
        return HttpResponse("False")


# func for running python script file from the external system storage
def external(request):

    # path of attendance.py file
    path = BASE_DIR + '/Attendance.py'
    out = run([sys.executable, path],
              shell=False, stdout=PIPE)
    # print(out.stdout)
    # return HttpResponseRedirect("external")
    return render(request, 'teacher_template/teacher_take_attendance_face.html')

def clear_csv_file(request):
    path = BASE_DIR + '/Attendance.csv'
    # path = '/home/vkkr125/programming/final_project/Final Project/Attendance_System/Attendance.csv'
    file = open(path, 'w+')
    file.close()
    with open(path, 'r+') as f:
        row = 'Name,' + 'Time,' + 'Date'
        f.writelines(row)
    return HttpResponseRedirect(reverse("teacher_take_attendance_face"))
    
#Using Pandas dataframe
def internal(request):
    # Read the csv file in
    csv_file_path = BASE_DIR + '/Attendance.csv'
    df = pd.read_csv(csv_file_path)
    # Save to file
    html_template_path = CUR_DIR + '/templates/teacher_template/Attendance.html'
    df.to_html(html_template_path)

    # Assign to string
    #html_file = (df.to_html(classes='table table-striped'))
    return HttpResponseRedirect(reverse("teacher_take_attendance_face"))
    # return render(request, 'teacher_template/teacher_take_attendance_face.html')
    
def readcsv(request):
    return render(request, 'teacher_template/Attendance.html')

def attendance_by_date(date):
    attendance_date = date
    attendance = Attendance.objects.get(id=attendance_date)
    attendance_data = AttendanceReport.objects.filter(attendance_id=attendance)
    list_data = []

    for student in attendance_data:
        data_small = {"id": student.student_id.admin.id,
                      "name": student.student_id.admin.first_name + " " + student.student_id.admin.last_name,
                      "status": student.status}
        list_data.append(data_small)
    return list_data


# preprocess the student data and put it into the .csv file
def get_attendance_by_subject(subject):
       # For Fetch All Student Under Teacher
    session_year_id = SessionYearModel.object.all()[0].id
    # print(session_year_id)
    subject_obj = Subjects.objects.get(id=subject)
    session_year_obj = SessionYearModel.object.get(id=session_year_id)
    attendance = Attendance.objects.filter(subject_id=subject_obj, session_year_id=session_year_obj)
    
    # attendance_single.attendance_date
    student_present_attendance_data = {}
    for attendance_single in attendance:
        list_data = attendance_by_date(attendance_single.id)
        for student_data in list_data : 
            # print(student_data['name'])
            if student_data['name'] in student_present_attendance_data:
                if student_data['status'] :
                    student_present_attendance_data[student_data['name']] += 1
            else:
                student_present_attendance_data[student_data['name']] = 0
    
    student_absent_attendance_data = {}
    for attendance_single in attendance:
        list_data = attendance_by_date(attendance_single.id)
        for student_data in list_data : 
            # print(student_data['name'])
            if student_data['name'] in student_absent_attendance_data:
                if not student_data['status'] :
                    student_absent_attendance_data[student_data['name']] += 1
            else:
                student_absent_attendance_data[student_data['name']] = 0
    
    return (student_present_attendance_data, student_absent_attendance_data)

def student_data_preprocessiong(request):
    subjects = Subjects.objects.filter(teacher_id=request.user.id)
    first_row = 'Student Name '
    for subject in subjects:
        first_row = first_row + ',' + subject.subject_name.split(' ')[0] + ' Attendance'
    # print(first_row)
    
    student_data_csv_path = BASE_DIR + '/student_info_data.csv'
    with open(student_data_csv_path, 'r+') as f:
        # f.writelines(first_row)

        subject_to_student_data = {}
        for subject in subjects:
            student_data_values_by_subject = get_attendance_by_subject(subject.id)
            keys = list(student_data_values_by_subject[0].keys())
            values1 = list(student_data_values_by_subject[0].values())
            values2 = list(student_data_values_by_subject[1].values())

            for i in range(0, len(keys)):
                if keys[i] in subject_to_student_data:
                    subject_to_student_data[keys[i]].append((subject.subject_name,values1[i],values2[i]))
                else:
                    subject_to_student_data[keys[i]] = [(subject.subject_name,values1[i], values2[i])]
        
        final_data = []
        subject_to_total_classes = {}
      
        for key in subject_to_student_data.keys():
            current_row = ''
            current_row += key 
            for value in subject_to_student_data[key]:
                current_row = current_row + ',' + str(value[1])

            for value in subject_to_student_data[key]:
                if value[0].split(' ')[0] in subject_to_total_classes:
                    subject_to_total_classes[value[0].split(' ')[0]] = max(subject_to_total_classes[value[0].split(' ')[0]], (value[1] + value[2]))
                else:
                    subject_to_total_classes[value[0].split(' ')[0]] = (value[1] + value[2])
            
            # f.writelines('\n' + current_row)
            final_data.append(current_row)
        
        total_classes = []
        for key,val in subject_to_total_classes.items():
            total_classes.append(val)
        
        final_first_row = 'Student Name'
        for col in first_row.split(','):
            if col.split(' ')[0] in subject_to_total_classes:
                final_first_row = final_first_row + ',' + col +  '(' + str(subject_to_total_classes[col.split(' ')[0]]) + ')'
        f.writelines(final_first_row)

        print(total_classes)

        for data in final_data :
            new_rows = data.split(',')
            new_str_row = new_rows[0]
            for i in range(1, len(new_rows)):
                precent = (int(new_rows[i]) / total_classes[i - 1] ) * 100
                new_str_row = new_str_row + ',' + str(precent) + '%'
    
            f.writelines('\n' + new_str_row)


        # print(subject_to_total_classes)
           
    return first_row
  

# fetch student attandance information and show the result in in excel format
def student_info_data(request):
    rows_data = student_data_preprocessiong(request)
    student_csv_data_path = BASE_DIR + '/student_info_data.csv'
    df = pd.read_csv(student_csv_data_path)

    student_data_template = CUR_DIR + '/templates/teacher_template/student_info_data.html'
    df.to_html(student_data_template)
    return render(request, 'teacher_template/student_info_data.html')


def save_face_attendance_data(request):


    subject = request.POST.get('subject')
    # read attendance.csv file,student fetch the students based on there name 
    # ans save the result to the database
    
    messages.success(request, "Attendance Data Saved Successfully!!")
    return HttpResponseRedirect(reverse('teacher_take_attendance_face'))