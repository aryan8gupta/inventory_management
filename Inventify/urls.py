from django.contrib import admin
from django.urls import path
from Inventify import settings
from django.conf.urls.static import static

from Inventify import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index),
    path('products-2/', views.products_2),

    path('login/', views.login),
    path('logout/', views.logout, name='logout'),


    path('dashboard/', views.dashboard),

    # Shop Owners ----------------------->
    path('employee/', views.employee),
    path('employee-signup/', views.employee_signup),
    
    path('products/', views.products),
    path('products-sold/', views.products_sold),
    
    path('products-add/', views.products_add),

    path('add-products/', views.add_products),
    path('upload', views.upload_image),

    path('contact/', views.contact_us),
    path('analytics/', views.analytics),

    path('barcode/', views.barcode),

    path('exchange/', views.exchange),
    path('sales/', views.sales),

    # For scanning QR-codes
    path('scan/', views.scan_qr, name='scan_qr'),
    
    # ----------------------------------->
    
    # Admin ----------------------->
    path('shops/', views.shops),
    path('shops-add/', views.shops_add),
    path('users-details/', views.users_details),
    path('users-signup/', views.users_signup),
    # ----------------------------------->
    
    path('delete/', views.delete),
    path('detail/', views.detail),
    path('update/', views.update),
    path('settings/', views.settings),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)