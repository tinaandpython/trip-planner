from django.urls import path
from .views import home, register, itinerary_generator, login, test_404, logout
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('itinerary_generator/', itinerary_generator, name = 'itinerary_generator'),
    # Django's built-in LogoutView class-based view handles the logout process automatically
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('test-404/', test_404, name='test_404'),
]