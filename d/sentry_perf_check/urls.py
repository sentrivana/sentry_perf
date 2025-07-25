from django.http import HttpResponse
from django.urls import path


def simple_view(request):
    return HttpResponse("Hello, world!")


async def simple_async_view(request):
    return HttpResponse("Hello from async view!")


urlpatterns = [
    path("hello", simple_view),
    path("hello-async", simple_async_view),
]
