from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from .forms import ItineraryGeneratorForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from .models import ItineraryGenerator
import requests



def home(request):
    return render(request, 'home.html')


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f'The username: {username} is already in use!')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                messages.success(request, 'Registration successful. You can now log in.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')
    return render(request, 'registration/register.html')



def login(request):
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('home')

def test_404(request):
    raise Http404("Testing custom 404 page")

@login_required
def itinerary_generator(request):
    if request.method == 'POST':
        if 'save' in request.POST:
            if 'itineraries' in request.session and 'destination' in request.session:
                itineraries = request.session['itineraries']
                destination = request.session['destination']

                # Save new data
                for i, day in enumerate(itineraries):
                    ItineraryGenerator.objects.create(
                        user=request.user,
                        destination=destination,
                        day=day['day'],
                        plan=day['activities']
                    )

                # Clear session data
                del request.session['itineraries']
                del request.session['destination']

                return redirect('itinerary_generator')
            else:
                return redirect('itinerary_generator')
        else:
            form = ItineraryGeneratorForm(request.POST)
            if form.is_valid():
                destination = form.cleaned_data['destination']
                days = form.cleaned_data['days']

                url = "https://ai-trip-planner.p.rapidapi.com/"
                querystring = {"days": str(days), "destination": destination}

                headers = {
                    "x-rapidapi-key": settings.RAPIDAPI_KEY,
                    "x-rapidapi-host": settings.RAPIDAPI_HOST,
                }

                response = requests.get(url, headers=headers, params=querystring)
                if response.status_code == 200:
                    data = response.json()

                # Stores the generated itineraries in a session, so I could use them for additional functionality
                request.session['itineraries'] = data['plan']
                request.session['destination'] = destination

                return render(request, 'itinerary_generator.html', {'itineraries': data['plan'], 'form': form, 'destination': destination})
            else:
                return render(request, 'itinerary_generator.html', {'form': form, 'error': 'Failed to retrieve data from the API.'})
    else:
        form = ItineraryGeneratorForm()

    return render(request, 'itinerary_generator.html', {'form': form})


@login_required
def saved_itineraries(request):
    itineraries = ItineraryGenerator.objects.filter(user=request.user)
    return render(request, 'saved_itineraries.html', {'itineraries': itineraries})