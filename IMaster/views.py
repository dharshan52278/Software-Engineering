from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group, auth
from .models import *
from  django.contrib import messages
import re
from django.contrib.auth.decorators import login_required
from .tasks import *
# Create your views here.

@login_required(login_url="info")
def home(request):
    courses = Course.objects.all()
    is_admin = request.user.groups.filter(name='Admin').exists()
    return render(request, "home.html", {"courses":courses, "is_admin":is_admin})

def intro(request):
    return render(request, "intro.html")

def base(request):
    return render(request, "base.html")    

def admins(request):
    is_admin = request.user.groups.filter(name='Admin').exists()
    error_message = None
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_obj = File.objects.create(file=uploaded_file)
        messages.info(request, "File uploaded")

        task_result = process_excel_file.delay(file_obj.id)
        if isinstance(task_result.result, str):
            error_message = task_result.result
    return render(request, "Admin/admins.html", {"is_admin":is_admin, 'error_message': error_message})         

def login(request):
    if request.user.is_authenticated :
      return redirect('home')

    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        try:
            user=auth.authenticate(username=username,password=password, email=email) 
            if user != None:
                auth.login(request,user)
                return redirect('home')
            else:
                messages.info(request, "Invalid credentials")
                return redirect('signup')
        except:
            return redirect('login')
 
    return render(request,'credentials/login.html')

def signup(request):
    details = User.objects.all()

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        con_password = request.POST.get('con_password')
        email = request.POST.get('email')

        EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9.]+[0-9]{2}[a-zA-Z]{2}@kct\.ac\.in$')
        
        if password == con_password:
          if EMAIL_PATTERN.match(email):
            if User.objects.filter(username=username).exists():
                messages.info(request, f"Username already exists")
                return redirect('signup')

            if User.objects.filter(email=email).exists():
                messages.info(request, f"Email already exists")
                return redirect('signup')

            user = User.objects.create_user(username=username, password=password, email=email)
            user = authenticate(username=username, password=password, email=email)
            student_group = Group.objects.get(name='Student')
            user.groups.add(student_group)

            info_id = request.session.get('info_id')
            if info_id:
                info = Info.objects.get(id=info_id)
                info.user = user
                info.save()
                del request.session['info_id']
            messages.success(request, "Account created successfully.")

            if user is not None:
                return redirect('login')
            else:
                messages.error(request, "Invalid username or password.")
          else:
            messages.error(request, "Email mismatched with pattern")     
        else:
          messages.error(request, "Password and Confirm Password are not matching")
    return render(request, 'credentials/signup.html')

def logout(request):
  auth.logout(request)
  return redirect('info')

def info(request):
  is_admin = request.user.groups.filter(name='Admin').exists()
  if request.method == "POST":
        institution_name = request.POST.get('institution_name')
        role = request.POST.get('role')
        
        if institution_name and role:
            info = Info.objects.create(institution_name=institution_name, role=role)
            request.session['info_id'] = info.id
            return redirect('signup')
        else:
            messages.error(request, "Please fill in all fields.")
  return render(request, "credentials/info.html", {"is_admin":is_admin})    

def view_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user

    progress, created = StudentCourseProgress.objects.get_or_create(student=user, course=course)
    completed_topics = progress.completed_topics.all()
    total_topics = course.topics.all()[:5]
    completed_count = completed_topics.filter(id__in=total_topics).count()
    progress_percentage = int((completed_count / len(total_topics)) * 100) if total_topics else 0
    is_admin = request.user.groups.filter(name='Admin').exists()

    context = {
        'course': course,
        'student_progress': progress,
        'progress': progress_percentage,
        'total_topics': total_topics,
        "is_admin": is_admin
    }
    
    return render(request, 'course/view_course.html', context)

def mark_topic_complete(request, course_id, topic_id):
    course = get_object_or_404(Course, id=course_id)
    topic = get_object_or_404(Topic, id=topic_id)
    user = request.user

    progress, created = StudentCourseProgress.objects.get_or_create(student=user, course=course)
    progress.completed_topics.add(topic)
    progress.save()

    return redirect('view_course', course_id=course_id)

def enroll_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user

    if user not in course.enrolled_students.all():
        course.enrolled_students.add(user)
        a = course.enrolled_students.all()
        for i in a:
          print(i)
        messages.success(request, f'You have successfully enrolled in {course.course_name}')
    else:
        messages.warning(request, f'You are already enrolled in {course.course_name}')

    return redirect('home')

def enrolled_courses(request):
    user = request.user
    enrolled_courses = user.enrolled_courses.all()
    is_admin = request.user.groups.filter(name='Admin').exists()
    return render(request, 'course/enrolled_courses.html', {'enrolled_courses': enrolled_courses, "is_admin":is_admin}) 

def course_overview(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    user = request.user

    progress, created = StudentCourseProgress.objects.get_or_create(student=user, course=course)
    completed_topics = progress.completed_topics.all()
    total_topics = course.topics.all()[:5]
    completed_count = completed_topics.filter(id__in=total_topics).count()
    is_admin = request.user.groups.filter(name='Admin').exists()

    context = {
        'course': course,
        'student_progress': progress,
        'total_topics': total_topics,
        "is_admin":is_admin
    }
    return render(request, "course/course_overview.html", context)

def timetable(request):
  is_admin = request.user.groups.filter(name='Admin').exists()
  return render(request, "timetable/students_timetable.html", {"is_admin":is_admin})

def cse_timetable(request):
  is_admin = request.user.groups.filter(name='Admin').exists()
  return render(request, "timetable/CSE_timetable.html", {"is_admin":is_admin}) 

def it_timetable(request):
  is_admin = request.user.groups.filter(name='Admin').exists()
  return render(request, "timetable/IT_timetable.html", {"is_admin":is_admin})  

def log(request):
    courses = Course.objects.all()
    return render(request, "Admin/admins.html", {'courses': courses})
  

  

