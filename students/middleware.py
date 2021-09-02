import time

from .models import Logger
from .views import create_student, edit_student


class PhoneValidatorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if (view_func == create_student or view_func == edit_student) and request.method == "POST" and (phone := request.POST.get('phone')): # noqa
            post = request.POST.copy()
            request.POST = post

            if not request.POST.get('phone').strip().isdigit():
                from django.contrib import messages
                request.POST.__setitem__('error', 666)
                messages.error(request, f"ERROR! {request.POST.get('phone')} -It's not a digit! Try again!")
            else:
                pass


class LogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        t1 = time.time()
        response = self.get_response(request)
        t2 = time.time()
        execution_time = t2-t1
        pattern = r"/admin/"

        if request.path.startswith(pattern):
            Logger.objects.create(
                method=request.method,
                path=request.path,
                execution_time=execution_time,
            )

        return response
