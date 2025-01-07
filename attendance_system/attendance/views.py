from django.shortcuts import render
from .face_recognition import capture_and_mark_attendance
from .models import Student, Attendance
from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from .face_recognition import register_new_user, mark_attendance_from_camera
# Create your views here.

def home(request):
    students = Student.objects.all()
    return render(request, 'attendance/home.html', {'students': students})


def mark_attendance(request):
    try:
        capture_and_mark_attendance()  # Call your face recognition script
    except ObjectDoesNotExist:
        return render(request, 'attendance/error.html', {
            'error_message': "No student found during attendance marking."
        })

    return render(request, 'attendance/attendance_marked.html')

def register(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:
            register_new_user(name)
            return redirect('home')
    return render(request, 'attendance/register.html')

def recognize_and_mark(request):
    mark_attendance_from_camera()
    return render(request, 'attendance/attendance_marked.html')