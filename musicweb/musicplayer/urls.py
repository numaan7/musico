from django.urls import path
from . import views
from django.conf.urls import handler404


handler404 = views.error404
urlpatterns = [
    path('',views.home,name='home'),
    path('mytracks/',views.my_tracks,name='mytracks'),
    path('tracks/',views.tracks,name='tracks'),
    path('contact-us/',views.contact,name="contact"),
    path('product/<int:id>/',views.product),
    path('status/',views.verify),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name= "logout"),
    path("blog/", views.blog, name= "blog"),
    path("blog/<int:id>/", views.blogdetails, name= "blogdetails"),
    path("blog/<str:url>/", views.blogdetails, name= "blogdetails"),
    path('search',views.search,name='search'),
    path('about-us',views.about,name='about-us'),

    
   
]
