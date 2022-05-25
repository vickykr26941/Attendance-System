from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin


class LoginCheckMiddleWare(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        modulename = view_func.__module__
        print(modulename)
        user = request.user
        if user.is_authenticated:
            if user.user_type == "1":
                if modulename == "Attendance_System_App.AdminViews":
                    pass
                elif modulename == "Attendance_System_App.views" or modulename == "django.views.static":
                    pass
                elif modulename == "django.contrib.auth.views" or modulename == "django.contrib.admin.sites":
                    pass
                else:
                    return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                if modulename == "Attendance_System_App.TeacherViews" or modulename == "Attendance_System_App.EditResultView":
                    pass
                elif modulename == "Attendance_System_App.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("teacher_home"))
            elif user.user_type == "3":
                if modulename == "Attendance_System_App.StudentServiceStaffViews":
                    pass
                elif modulename == "Attendance_System_App.views" or modulename == "django.views.static":
                    pass
                else:
                    return HttpResponseRedirect(reverse("studentservicestaff_home"))
            elif user.user_type == "4":
                if modulename == "Attendance_System_App.StudentViews" or modulename == "django.views.static":
                    pass
                elif modulename == "Attendance_System_App.views":
                    pass
                else:
                    return HttpResponseRedirect(reverse("student_home"))
            else:
                return HttpResponseRedirect(reverse("show_login"))

        else:
            if request.path == reverse("show_login") or request.path == reverse(
                    "do_login") or modulename == "django.contrib.auth.views" or modulename == "django.contrib.admin" \
                                                                                              ".sites" or modulename \
                    == "Attendance_System_App.views" or modulename =="Attendance_System_App.views":
                pass
            else:
                return HttpResponseRedirect(reverse("show_login"))

