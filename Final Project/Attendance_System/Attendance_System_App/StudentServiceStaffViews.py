import json
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse

from Attendance_System_App.models import CustomUser, StudentServiceStaffs, FeedBackStudents, Subjects, SessionYearModel, Attendance, AttendanceReport

from django.views.decorators.csrf import csrf_exempt

from Attendance_System_App.models import Students, Teachers, Courses, LeaveReportTeachers, LeaveReportStudents


def studentservicestaff_home(request):
    student_count1 = Students.objects.all().count()
    teacher_count = Teachers.objects.all().count()
    subject_count = Subjects.objects.all().count()
    course_count = Courses.objects.all().count()

    course_all = Courses.objects.all()
    course_name_list = []
    subject_count_list = []
    student_count_list_in_course = []
    for course in course_all:
        subjects = Subjects.objects.filter(course_id=course.id).count()
        students = Students.objects.filter(course_id=course.id).count()
        course_name_list.append(course.course_name)
        subject_count_list.append(subjects)
        student_count_list_in_course.append(students)

    subjects_all = Subjects.objects.all()
    subject_list = []
    student_count_list_in_subject = []
    for subject in subjects_all:
        course = Courses.objects.get(id=subject.course_id.id)
        student_count = Students.objects.filter(course_id=course.id).count()
        subject_list.append(subject.subject_name)
        student_count_list_in_subject.append(student_count)

    teachers = Teachers.objects.all()
    attendance_present_list_teacher = []
    attendance_absent_list_teacher = []
    teacher_name_list = []
    for teacher in teachers:
        subject_ids = Subjects.objects.filter(teacher_id=teacher.admin.id)
        attendance = Attendance.objects.filter(subject_id__in=subject_ids).count()
        leaves = LeaveReportTeachers.objects.filter(teacher_id=teacher.id, leave_status=1).count()
        attendance_present_list_teacher.append(attendance)
        attendance_absent_list_teacher.append(leaves)
        teacher_name_list.append(teacher.admin.username)

    students_all = Students.objects.all()
    attendance_present_list_student = []
    attendance_absent_list_student = []
    student_name_list = []
    for student in students_all:
        attendance = AttendanceReport.objects.filter(student_id=student.id, status=True).count()
        absent = AttendanceReport.objects.filter(student_id=student.id, status=False).count()
        leaves = LeaveReportStudents.objects.filter(student_id=student.id, leave_status=1).count()
        attendance_present_list_student.append(attendance)
        attendance_absent_list_student.append(leaves + absent)
        student_name_list.append(student.admin.username)

    return render(request, "studentservicestaff_template/studentservicestaff_home_template.html",
                  {"student_count": student_count1, "teacher_count": teacher_count, "subject_count": subject_count,
                   "course_count": course_count, "course_name_list": course_name_list,
                   "subject_count_list": subject_count_list,
                   "student_count_list_in_course": student_count_list_in_course,
                   "student_count_list_in_subject": student_count_list_in_subject, "subject_list": subject_list,
                   "teacher_name_list": teacher_name_list,
                   "attendance_present_list_teacher": attendance_present_list_teacher,
                   "attendance_absent_list_teacher": attendance_absent_list_teacher,
                   "student_name_list": student_name_list,
                   "attendance_present_list_student": attendance_present_list_student,
                   "attendance_absent_list_student": attendance_absent_list_student})



def studentservicestaff_profile(request):
    user=CustomUser.objects.get(id=request.user.id)
    studentservicestaff=StudentServiceStaffs.objects.get(admin=user)
    return render(request,"studentservicestaff_template/studentservicestaff_profile.html",{"user":user,"studentservicestaff":studentservicestaff})

def studentservicestaff_profile_save(request):
    if request.method!="POST":
        return HttpResponseRedirect(reverse("studentservicestaff_profile"))
    else:
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        address=request.POST.get("address")
        password=request.POST.get("password")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            if password!=None and password!="":
                customuser.set_password(password)
            customuser.save()

            studentservicestaff=StudentServiceStaffs.objects.get(admin=customuser.id)
            studentservicestaff.address=address
            studentservicestaff.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("studentservicestaff_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("studentservicestaff_profile"))


def student_feedback_message_sss(request):
    feedbacks = FeedBackStudents.objects.all()
    return render(request, "studentservicestaff_template/student_feedback_template.html", {"feedbacks": feedbacks})


def sss_view_attendance(request):
    subjects = Subjects.objects.all()
    session_year_id = SessionYearModel.object.all()
    return render(request, "studentservicestaff_template/sss_view_attendance.html", {"subjects": subjects, "session_year_id": session_year_id})


# view attendance admin
@csrf_exempt
def sss_get_attendance_dates(request):
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
def sss_get_attendance_student(request):
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

