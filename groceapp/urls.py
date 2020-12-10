from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth.views import LoginView, LogoutView 


urlpatterns = [
    path('',views.home,name='home'),
    path('accounts/register/', views.registration, name='register'),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('profile/<username>/',views.profile, name='profile'),
    path('profile/<username>/update/',views.update_profile, name='update_profile'), 
    path('<category_id>/new-unit/', views.add_unit, name='new-unit'),
    path('unit-info/<category_id>/<username>/', views.units_info, name='units-info'),
    
]