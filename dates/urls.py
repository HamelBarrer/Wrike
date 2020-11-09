from django.urls import path

from . import views

app_name = 'dates'
urlpatterns = [
    path('<pk>/', views.DeveloperDatailView.as_view(), name='date'),
]
