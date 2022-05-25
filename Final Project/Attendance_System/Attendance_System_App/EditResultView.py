from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import View

from Attendance_System_App.forms import EditResultForm
from Attendance_System_App.models import Students, Subjects, StudentResult


class EditResultViewClass(View):
    def get(self,request,*args,**kwargs):
        teacher_id=request.user.id
        edit_result_form=EditResultForm(teacher_id=teacher_id)
        return render(request,"teacher_template/edit_student_result.html",{"form":edit_result_form})

    def post(self,request,*args,**kwargs):
        form=EditResultForm(teacher_id=request.user.id,data=request.POST)
        if form.is_valid():
            student_admin_id = form.cleaned_data['student_ids']
            assignment_marks = form.cleaned_data['assignment_marks']
            exam_marks = form.cleaned_data['exam_marks']
            subject_id = form.cleaned_data['subject_id']

            student_obj = Students.objects.get(admin=student_admin_id)
            subject_obj = Subjects.objects.get(id=subject_id)
            result=StudentResult.objects.get(subject_id=subject_obj,student_id=student_obj)
            result.subject_assignment_marks=assignment_marks
            result.subject_exam_marks=exam_marks
            result.save()
            messages.success(request, "Successfully Updated Result")
            return HttpResponseRedirect(reverse("edit_student_result"))
        else:
            messages.error(request, "Failed to Update Result")
            form=EditResultForm(request.POST,teacher_id=request.user.id)
            return render(request,"teacher_template/edit_student_result.html",{"form":form})
