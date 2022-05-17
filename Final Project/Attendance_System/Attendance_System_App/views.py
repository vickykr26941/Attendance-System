import json
import requests
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from Attendance_System_App.EmailBackEnd import EmailBackEnd

from Attendance_System_App.models import CustomUser, Courses, SessionYearModel


def ShowLoginPage(request):
    return render(request, "login_page.html")


def doLogin(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        ## uncomment this line to apply google captch in login system
        # captcha_token=request.POST.get("g-recaptcha-response")
        # cap_url="https://www.google.com/recaptcha/api/siteverify"
        # cap_secret="6LfkArAaAAAAADp-yIkgGt-dPQypVV8cOnYGIYtB"
        # cap_data={"secret":cap_secret, "response":captcha_token}
        # cap_server_response=requests.post(url=cap_url, data=cap_data)
        # cap_json = json.loads(cap_server_response.text)

        # if cap_json['success'] == False:
        #     messages.error(request, "Invalid Captcha Try Again")
        #     return HttpResponseRedirect("/")
        print(request.POST.get('email'))
        user = EmailBackEnd.authenticate(request, username=request.POST.get("email"),
                                         password=request.POST.get("password"))
        # if(user.size() > 0) : 
        #     return HttpResponse('Too Many Users with the same email')

        if user != None:
            login(request, user)
            if user.user_type == "1":
                return HttpResponseRedirect(reverse("admin_home"))
            elif user.user_type == "2":
                return HttpResponseRedirect(reverse("teacher_home"))
            elif user.user_type == "3":
                return HttpResponseRedirect(reverse("studentservicestaff_home"))
            else:
                return HttpResponseRedirect(reverse("student_home"))
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")


def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("user : " + request.user.email + " usertype : " + request.user.user_type)
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

def Testurl(request):
    return HttpResponse("Ok")


def register_admin(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")
    
    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=1)
        user.save()
        messages.success(request,"Successfully Created Admin")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request,"Failed to Create Admin")
        return HttpResponseRedirect(reverse("show_login"))

def register_teacher(request):
    return render(request,"register_teacher_page.html")


def do_register_teacher(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")
    address=request.POST.get("address")

    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=2)
        user.teachers.address=address
        user.save()
        messages.success(request,"Successfully Created Teacher")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request,"Failed to Create Teacher")
        return HttpResponseRedirect(reverse("show_login"))

def register_studentservicestaff(request):
    return render(request,"register_studentservicestaff_page.html")

def do_register_studentservicestaff(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")
    address=request.POST.get("address")

    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=3)
        user.studentservicestaffs.address=address
        user.save()
        messages.success(request,"Successfully Created Student Service Staff")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request,"Failed to Create Student Service Staff")
        return HttpResponseRedirect(reverse("show_login"))

def register_student(request):
    courses = Courses.objects.all()
    session_years = SessionYearModel.object.all()
    return render(request, "register_student_page.html", {"courses": courses, "session_years": session_years})

def do_register_student(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    address = request.POST.get("address")
    session_year_id = request.POST.get("session_year")
    course_id = request.POST.get("course")
    sex = request.POST.get("sex")

    profile_pic = request.FILES['profile_pic']
    fs = FileSystemStorage()
    filename = fs.save(profile_pic.name, profile_pic)
    profile_pic_url = fs.url(filename)


    user = CustomUser.objects.create_user(username=username, password=password, email=email, last_name=last_name,
                                          first_name=first_name, user_type=4)
    user.students.address = address
    course_obj = Courses.objects.get(id=course_id)
    user.students.course_id = course_obj
    session_year = SessionYearModel.object.get(id=session_year_id)
    user.students.session_year_id = session_year
    user.students.gender = sex
    user.students.profile_pic = profile_pic_url
    user.save()
    messages.success(request, "Successfully Added Student")
    return HttpResponseRedirect(reverse("show_login"))
