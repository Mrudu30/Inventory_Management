from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('signin/',views.signin,name='signin'),
    path('signout/',views.signout,name='signout'),
    path('signup/',views.signup,name='signup'),
    path('profile/',views.profile,name='profile'),
    path('edit_details/=?<str:pk>/',views.edit_user,name='edit_details'),
    path('inventory/<str:pk>/',views.inventory,name='inventory'),
    path('edit_inventory/<str:pk>/',views.edit_inventory,name='edit_inventory'),
]
