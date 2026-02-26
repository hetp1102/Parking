
from django.urls import path
from . import views
urlpatterns = [
 path('', views.home, name='home'),
 path('signup/', views.signup_view, name='signup'),
 path('login/', views.login_view, name='login'),
 path('logout/', views.logout_view, name='logout'),
 path('dashboard/', views.dashboard, name='dashboard'),
 path('staff/', views.staff_dashboard, name='staff_dashboard'),
 path('staff/scanner/', views.staff_scanner, name='staff_scanner'),
 path('admin-profile/', views.admin_profile, name='admin_profile'),
]
