from django.urls import path
from .views import home, register, login, test_404, itinerary_generator, saved_itineraries, delete_itinerary
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('itinerary_generator/', itinerary_generator, name = 'itinerary_generator'),
    # Django's built-in LogoutView class-based view handles the logout process automatically
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('saved-itineraries/', saved_itineraries, name='saved_itineraries'),
    path('saved-itineraries/delete/<int:itinerary_id>/', delete_itinerary, name='delete_itinerary'),
    path('test-404/', test_404, name='test_404'),
]