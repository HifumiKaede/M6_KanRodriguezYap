from django.urls import path
from . import views

urlpatterns = [
    # ACCOUNT
    path('', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('basic_list/<int:pk>/', views.basic_list, name='basic_list'),
    path('manage_account/<int:pk>/', views.manage_account, name='manage_account'),
    path('change_password/<int:pk>/', views.change_password, name='change_password'),
    path('delete_account/<int:pk>/', views.delete_account, name='delete_account'),
    path('logout/', views.logout_view, name='logout'),

    # DISH
    path('menu/', views.better_menu, name='better_menu'),
    path('menu/add/', views.add_menu, name='add_menu'),
    path('menu/view/<int:pk>/', views.view_detail, name='view_detail'),
    path('menu/update/<int:pk>/', views.update_dish, name='update_dish'),
    path('menu/delete/<int:pk>/', views.delete_dish, name='delete_dish'),
]
