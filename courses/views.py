from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg
from .models import Course, Category, Lesson, Comment, Enrollment


def home(request):
    featured_courses = Course.objects.filter(is_published=True)[:6]
    categories = Category.objects.annotate(course_count=Count('courses'))[:6]
    total_courses = Course.objects.filter(is_published=True).count()
    total_students = Enrollment.objects.values('user').distinct().count()

    context = {
        'featured_courses': featured_courses,
        'categories': categories,
        'total_courses': total_courses,
        'total_students': total_students,
    }
    return render(request, 'courses/home.html', context)


def course_list(request):
    courses = Course.objects.filter(is_published=True).annotate(
        student_count=Count('students'),
        avg_rating=Avg('comments__rating')
    )

    category_slug = request.GET.get('category')
    level = request.GET.get('level')
    search = request.GET.get('search')

    if category_slug:
        courses = courses.filter(category__slug=category_slug)
    if level:
        courses = courses.filter(level=level)
    if search:
        courses = courses.filter(title__icontains=search)

    categories = Category.objects.all()

    context = {
        'courses': courses,
        'categories': categories,
    }
    return render(request, 'courses/course_list.html', context)


def course_detail(request, slug):
    course = get_object_or_404(Course, slug=slug, is_published=True)
    lessons = course.lessons.all()
    comments = course.comments.select_related('user')[:10]
    is_enrolled = request.user.is_authenticated and course.students.filter(id=request.user.id).exists()

    context = {
        'course': course,
        'lessons': lessons,
        'comments': comments,
        'is_enrolled': is_enrolled,
    }
    return render(request, 'courses/course_detail.html', context)


@login_required
def enroll_course(request, slug):
    course = get_object_or_404(Course, slug=slug)

    if course.students.filter(id=request.user.id).exists():
        messages.info(request, 'Vous êtes déjà inscrit à ce cours.')
    else:
        course.students.add(request.user)
        Enrollment.objects.create(user=request.user, course=course)
        messages.success(request, f'Vous êtes inscrit au cours "{course.title}"!')

    return redirect('course_detail', slug=slug)


@login_required
def lesson_detail(request, course_slug, lesson_slug):
    course = get_object_or_404(Course, slug=course_slug)
    lesson = get_object_or_404(Lesson, course=course, slug=lesson_slug)

    is_enrolled = course.students.filter(id=request.user.id).exists()

    if not is_enrolled and not lesson.is_preview:
        messages.error(request, 'Vous devez être inscrit pour accéder à cette leçon.')
        return redirect('course_detail', slug=course_slug)

    lessons = course.lessons.all()

    context = {
        'course': course,
        'lesson': lesson,
        'lessons': lessons,
    }
    return render(request, 'courses/lesson_detail.html', context)


@login_required
def add_comment(request, slug):
    if request.method == 'POST':
        course = get_object_or_404(Course, slug=slug)
        content = request.POST.get('content')
        rating = request.POST.get('rating', 5)

        Comment.objects.create(
            course=course,
            user=request.user,
            content=content,
            rating=rating
        )
        messages.success(request, 'Votre commentaire a été ajouté!')

    return redirect('course_detail', slug=slug)


@login_required
def my_courses(request):
    enrollments = Enrollment.objects.filter(user=request.user).select_related('course')

    context = {
        'enrollments': enrollments,
    }
    return render(request, 'courses/my_courses.html', context)