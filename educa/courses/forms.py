from django import forms
from django.forms.models import inlineformset_factory
from .models import Course, Module

# Define an inline formset for the Module model related to a Course model
ModuleFormSet = inlineformset_factory(
    Course,  # Parent model
    Module,  # Related model
    fields=['title', 'description'],  # Fields to include in the formset
    extra=2,  # Number of empty forms to display
    can_delete=True  # Allow deletion of existing related objects
)
