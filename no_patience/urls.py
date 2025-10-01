from django.urls import path


from . import views

app_name = 'no_patience'
urlpatterns = [
    # Home page.
    path('', views.index, name='index'),
]
