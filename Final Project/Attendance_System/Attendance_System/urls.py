"""Attendance_System URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, re_path
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from Attendance_System import settings
from Attendance_System_App import views, AdminViews, TeacherViews, StudentViews, StudentServiceStaffViews

from Attendance_System_App.EditResultView import EditResultViewClass


urlpatterns = [


    # utility urls
    path('register_student',views.register_student,name="register_student"),
    path('register_teacher',views.register_teacher,name="register_teacher"),
    path('register_studentservicestaff',views.register_studentservicestaff,name="register_studentservicestaff"),
    path('do_register_student', views.do_register_student, name="do_register_student"),
    path('do_register_teacher', views.do_register_teacher, name="do_register_teacher"),
    path('do_register_studentservicestaff', views.do_register_studentservicestaff,name="do_register_studentservicestaff"),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.ShowLoginPage, name="show_login"),
    path('doLogin', views.doLogin, name="do_login"),
    path('get_user_details', views.GetUserDetails),
    path('logout_user', views.logout_user, name="logout"),
    path('admin_home', AdminViews.admin_home, name="admin_home"),
    path('add_teacher', AdminViews.add_teacher, name="add_teacher"),
    path('add_teacher_save', AdminViews.add_teacher_save, name="add_teacher_save"),
    path('add_student_service_staff', AdminViews.add_student_service_staff, name="add_student_service_staff"),
    path('add_student_service_staff_save', AdminViews.add_student_service_staff_save, name="add_student_service_staff_save"),
    path('add_course', AdminViews.add_course, name="add_course"),
    path('add_course_save', AdminViews.add_course_save, name="add_course_save"),
    path('add_student', AdminViews.add_student, name="add_student"),
    path('add_student_save', AdminViews.add_student_save, name="add_student_save"),
    path('add_subject', AdminViews.add_subject, name="add_subject"),
    path('add_subject_save', AdminViews.add_subject_save, name="add_subject_save"),
    path('manage_teacher', AdminViews.manage_teacher, name="manage_teacher"),
    path('manage_student', AdminViews.manage_student, name="manage_student"),
    path('manage_student_service_staff', AdminViews.manage_student_service_staff, name="manage_student_service_staff"),
    path('manage_course', AdminViews.manage_course, name="manage_course"),
    path('manage_subject', AdminViews.manage_subject, name="manage_subject"),
    path('edit_teacher_save', AdminViews.edit_teacher_save, name="edit_teacher_save"),
    path('edit_student_service_staff/<str:studentservicestaff_id>', AdminViews.edit_student_service_staff, name="edit_student_service_staff"),
    path('edit_student_service_staff_save', AdminViews.edit_student_service_staff_save, name="edit_student_service_staff_save"),
    path('edit_student_save', AdminViews.edit_student_save, name="edit_student_save"),
    path('edit_subject_save', AdminViews.edit_subject_save, name="edit_subject_save"),
    path('edit_course_save', AdminViews.edit_course_save, name="edit_course_save"),
    path('manage_session', AdminViews.manage_session, name="manage_session"),
    path('add_session_save', AdminViews.add_session_save, name="add_session_save"),
    path('check_email_exist', AdminViews.check_email_exist, name="check_email_exist"),
    path('check_username_exist', AdminViews.check_username_exist, name="check_username_exist"),
    path('student_feedback_message', AdminViews.student_feedback_message, name="student_feedback_message"),
    path('student_feedback_message_replied', AdminViews.student_feedback_message_replied, name="student_feedback_message_replied"),
    path('teacher_feedback_message', AdminViews.teacher_feedback_message, name="teacher_feedback_message"),
    path('teacher_feedback_message_replied', AdminViews.teacher_feedback_message_replied, name="teacher_feedback_message_replied"),
    path('student_leave_view', AdminViews.student_leave_view, name="student_leave_view"),
    path('teacher_leave_view', AdminViews.teacher_leave_view, name="teacher_leave_view"),


    # dynamic urls with Id's
    path('edit_course/<str:course_id>', AdminViews.edit_course, name="edit_course"),
    path('edit_subject/<str:subject_id>', AdminViews.edit_subject, name="edit_subject"),
    path('edit_teacher/<str:teacher_id>', AdminViews.edit_teacher, name="edit_teacher"),
    path('edit_student/<str:student_id>', AdminViews.edit_student, name="edit_student"),
    path('student_approve_leave/<str:leave_id>', AdminViews.student_approve_leave, name="student_approve_leave"),
    path('student_disapprove_leave/<str:leave_id>', AdminViews.student_disapprove_leave, name="student_disapprove_leave"),
    path('teacher_approve_leave/<str:leave_id>', AdminViews.teacher_approve_leave, name="teacher_approve_leave"),
    path('teacher_disapprove_leave/<str:leave_id>', AdminViews.teacher_disapprove_leave, name="teacher_disapprove_leave"),


    path('admin_view_attendance', AdminViews.admin_view_attendance, name="admin_view_attendance"),
    path('admin_get_attendance_dates', AdminViews.admin_get_attendance_dates, name="admin_get_attendance_dates"),
    path('admin_get_attendance_student', AdminViews.admin_get_attendance_student, name="admin_get_attendance_student"),
    path('admin_profile', AdminViews.admin_profile, name="admin_profile"),
    path('admin_profile_save', AdminViews.admin_profile_save, name="admin_profile_save"),

    #<<<<<<<<< Teacher URL Path >>>>>>>>>
    path('teacher_home', TeacherViews.teacher_home, name="teacher_home"),
    path('teacher_take_attendance', TeacherViews.teacher_take_attendance, name="teacher_take_attendance"),
    path('teacher_take_attendance_face', TeacherViews.teacher_take_attendance_face, name="teacher_take_attendance_face"),
    re_path(r'^external', TeacherViews.external,name="script"), #face recogntion url and func in Teachersview
    re_path(r'^internal', TeacherViews.internal, name="button"),
    path('student_info_data', TeacherViews.student_info_data, name='student_info_data'),
    path('clear_csv_file',TeacherViews.clear_csv_file, name='clear_csv_file'),

    path('readcsv', TeacherViews.readcsv, name="readcsv"),

    path('teacher_update_attendance', TeacherViews.teacher_update_attendance, name="teacher_update_attendance"),
    path('teacher_apply_leave', TeacherViews.teacher_apply_leave, name="teacher_apply_leave"),
    path('teacher_apply_leave_save', TeacherViews.teacher_apply_leave_save,name="teacher_apply_leave_save"),
    path('teacher_feedback', TeacherViews.teacher_feedback, name="teacher_feedback"),
    path('teacher_feedback_save', TeacherViews.teacher_feedback_save, name="teacher_feedback_save"),
    path('teacher_profile', TeacherViews.teacher_profile, name="teacher_profile"),
    path('teacher_profile_save', TeacherViews.teacher_profile_save, name="teacher_profile_save"),
    path('get_students', TeacherViews.get_students, name="get_students"),
    path('get_attendance_dates', TeacherViews.get_attendance_dates, name="get_attendance_dates"),
    path('get_attendance_student', TeacherViews.get_attendance_student, name="get_attendance_student"),
    path('save_attendance_data', TeacherViews.save_attendance_data, name="save_attendance_data"),
    path('save_update_attendance_data', TeacherViews.save_update_attendance_data, name="save_update_attendance_data"),
    path('student_leave_view1', TeacherViews.student_leave_view1, name="student_leave_view1"),
    path('student_approve_leave/<str:leave_id>', TeacherViews.student_approve_leave, name="student_approve_leave"),
    path('student_disapprove_leave/<str:leave_id>', TeacherViews.student_disapprove_leave, name="student_disapprove_leave"),
    path('teacher_add_result', TeacherViews.teacher_add_result, name="teacher_add_result"),
    path('save_student_result', TeacherViews.save_student_result, name="save_student_result"),
    path('edit_student_result', EditResultViewClass.as_view(), name="edit_student_result"),
    path('fetch_result_student', TeacherViews.fetch_result_student, name="fetch_result_student"),
    path('save_face_attendance_data', TeacherViews.save_face_attendance_data, name="save_face_attendance_data"),

    # <<<<<<<< Student URL Path >>>>>>>>>>
    path('student_home', StudentViews.student_home, name="student_home"),
    path('student_view_attendance', StudentViews.student_view_attendance, name="student_view_attendance"),
    path('student_view_attendance_post', StudentViews.student_view_attendance_post, name="student_view_attendance_post"),
    path('student_apply_leave', StudentViews.student_apply_leave, name="student_apply_leave"),
    path('student_apply_leave_save', StudentViews.student_apply_leave_save, name="student_apply_leave_save"),
    path('student_feedback', StudentViews.student_feedback, name="student_feedback"),
    path('student_feedback_save', StudentViews.student_feedback_save, name="student_feedback_save"),
    path('student_profile', StudentViews.student_profile, name="student_profile"),
    path('student_profile_save', StudentViews.student_profile_save, name="student_profile_save"),
    path('student_view_result', StudentViews.student_view_result, name="student_view_result"),

    # <<<<<<<<<<< Student Service Staff URL Path >>>>>>>>>>>
    path('studentservicestaff_home', StudentServiceStaffViews.studentservicestaff_home, name="studentservicestaff_home"),
    path('studentservicestaff_profile', StudentServiceStaffViews.studentservicestaff_profile, name="studentservicestaff_profile"),
    path('studentservicestaff_profile_save', StudentServiceStaffViews.studentservicestaff_profile_save, name="studentservicestaff_profile_save"),
    path('student_feedback_message_sss', StudentServiceStaffViews.student_feedback_message_sss, name="student_feedback_message_sss"),
    path('sss_view_attendance', StudentServiceStaffViews.sss_view_attendance, name="sss_view_attendance"),
    path('sss_get_attendance_dates', StudentServiceStaffViews.sss_get_attendance_dates, name="sss_get_attendance_dates"),
    path('sss_get_attendance_student', StudentServiceStaffViews.sss_get_attendance_student, name="sss_get_attendance_student"),
    path('testurl',views.Testurl),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

