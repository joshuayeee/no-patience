from django.urls import path


from . import views

app_name = 'no_patience'
urlpatterns = [
    # Home page.
    path('', views.index, name='index'),
    path('chat', views.chat, name='chat'),
    path('navbar', views.navbar, name='navbar'),
    path('sidebar', views.sidebar, name='sidebar'),
]
