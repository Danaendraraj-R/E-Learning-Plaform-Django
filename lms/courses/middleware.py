from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from .models import Course

def subdomain_course_middleware(get_response):
    """
    Middleware to handle subdomains for courses.
    """
    def middleware(request):
        host_parts = request.get_host().split('.')
        
        # Check if there are more than two parts in the host and the first part is not 'www'
        if len(host_parts) > 2 and host_parts[0] != 'www':
            # Get the course for the given subdomain
            course = get_object_or_404(Course, slug=host_parts[0])
            # Generate the URL for the course detail view
            course_url = reverse('course_detail', args=[course.slug])
            # Construct the full URL with the scheme and adjusted subdomain
            url = '{}://{}{}'.format(request.scheme, '.'.join(host_parts[1:]), course_url)
            # Redirect current request to the course_detail view
            return redirect(url)
        
        # If no subdomain match, continue with the request
        response = get_response(request)
        return response
    
    return middleware
