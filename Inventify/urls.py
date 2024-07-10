from django.contrib import admin
from django.urls import path

from Inventify import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index),
    path('home/', views.home),

    path('login/', views.login),
    path('logout/', views.logout, name='logout'),


    path('dashboard/', views.dashboard),

    # Shop Owners ----------------------->
    path('employee/', views.employee),
    path('employee-signup/', views.employee_signup),
    
    path('products/', views.products),
    path('products-sold/', views.products_sold),
    path('products-add/', views.products_add),

    path('contact/', views.contact_us),

    path('barcode/', views.barcode),
    # ----------------------------------->
    
    # Admin ----------------------->
    path('shops/', views.shops),
    path('shops-add/', views.shops_add),
    path('users-details/', views.users_details),
    path('users-signup/', views.users_signup),
    # ----------------------------------->
]