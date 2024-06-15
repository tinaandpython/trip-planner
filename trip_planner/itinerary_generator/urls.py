from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('itinerary_generator/', views.itinerary_generator, name = 'itinerary_generator'),
    # Django's built-in LogoutView class-based view handles the logout process automatically
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('saved-itineraries/', views.saved_itineraries, name='saved_itineraries'),
    path('itinerary/<int:itinerary_id>/', views.itinerary_detail, name='itinerary_detail'),
    path('saved-itineraries/itinerary/<int:itinerary_id>/delete', views.delete_itinerary, name='delete_itinerary'),
    path('saved-itineraries/itinerary/<int:itinerary_id>/confirm-delete/', views.confirm_itinerary_deletion, name='confirm_itinerary_deletion'),
    path('test-404/', views.test_404, name='test_404'),
]