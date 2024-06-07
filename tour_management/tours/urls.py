from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('packages/', views.package_list, name='package_list'),
    path('packages/<int:pk>/', views.package_detail, name='package_detail'),
    path('book/<int:pk>/', views.book_package, name='book_package'),
    path('payment/<int:pk>/', views.payment, name='payment'),
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('vendor/manage_package/', views.manage_package, name='create_package'),
    path('vendor/manage_package/<int:pk>/', views.manage_package, name='manage_package'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/approve_package/<int:pk>/', views.approve_package, name='approve_package'),
]