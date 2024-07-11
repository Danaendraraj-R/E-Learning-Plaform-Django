from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CourseEnrollForm
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.shortcuts import get_object_or_404
from courses.models import Course, Module


class StudentRegistrationView(CreateView):
    template_name = 'students/student/registration.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('student_course_list')
    def form_valid(self, form):
        result = super().form_valid(form)
        cd = form.cleaned_data
        user = authenticate(username=cd['username'],
        password=cd['password1'])
        login(self.request, user)
        return result

class StudentEnrollCourseView(LoginRequiredMixin, FormView):
    course = None
    form_class = CourseEnrollForm
    def form_valid(self, form):
        self.course = form.cleaned_data['course']
        self.course.students.add(self.request.user)
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('student_course_detail',args=[self.course.id])
    
class StudentCourseListView(LoginRequiredMixin, ListView):
    model = Course
    template_name = 'students/course/list.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students__in=[self.request.user])
    
class StudentCourseDetailView(DetailView):
    model = Course
    template_name = 'students/course/detail.html'
    context_object_name = 'course'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(students=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = self.get_object()

        # Check if module_id is provided in URL params
        module_id = self.kwargs.get('module_id')
        if module_id:
            # Display specific module details
            module = get_object_or_404(Module, id=module_id, course=course)
            context['module'] = module
        else:
            # Display default module (e.g., first module)
            context['module'] = course.modules  # Adjust as per your logic

        return context
