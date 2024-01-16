from django.urls import path
from .views import download_video

urlpatterns = [
    # Your other URL patterns go here

    # Add the URL pattern for the download_video view
    path('download_video/', download_video, name='download_video'),
]

