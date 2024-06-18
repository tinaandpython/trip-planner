from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.core.exceptions import ValidationError
from django.contrib import messages
from .forms import ItineraryGeneratorForm
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout, update_session_auth_hash
from .models import ItineraryGenerator
import requests
import re



def home(request):
    return render(request, 'home.html')

def validate_password(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not re.search(r"[A-Za-z]", password):
        raise ValidationError("Password must contain at least one letter.")
    if not re.search(r"[0-9]", password):
        raise ValidationError("Password must contain at least one number.")

@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            try:
                validate_password(password)
            except ValidationError as e:
                messages.error(request, ' '.join(e.messages))
                return redirect('register')

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
        # Checks if the 'save' button was pressed
        if 'save' in request.POST:
            # session aka browsing session (cookies). When data is stored in request.session,
            # it is saved on the server side and associated with a session ID.
            # The session ID is sent to the client as a cookie.
            if 'itineraries' in request.session and 'destination' in request.session:
                itineraries = request.session['itineraries']
                destination = request.session['destination']
                days = request.session['days']

                # test
                # print("Session itineraries:", itineraries)
                # print("Session destination:", destination)

                api_response = {
                    'itineraries': itineraries,
                    'destination': destination
                }

                # Saving new data
                ItineraryGenerator.objects.create(
                    user=request.user,
                    destination=destination,
                    days=days,
                    api_response=api_response
                )

                # Clear session data after it's saved on the db
                del request.session['itineraries']
                del request.session['destination']
                del request.session['days']

                # success message if the itinerary has been saved (django built-in messages)
                messages.success(request, 'Your itinerary has been saved!')

                return redirect('itinerary_generator')
            else:
                #print("Session data missing") --> test
                # failure message if session capture fails
                messages.error(request, 'Session data is missing. Please try again.')
                return redirect('itinerary_generator')
        else:
            # Handles form submission ItineraryGenerator
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
                    #print("API response data:", data)
                else:
                    #print("Failed API request:", response.status_code, response.text)
                    data = {'plan': []}  # Handles failed response case, places an empty list

                # Stores the generated itineraries in a session
                request.session['itineraries'] = data['plan']
                request.session['destination'] = destination
                request.session['days'] = days

                return render(request, 'itinerary_generator.html', {'itineraries': data['plan'], 'form': form, 'destination': destination})
            else:
                print("Form is invalid")
                return render(request, 'itinerary_generator.html', {'form': form, 'error': 'Failed to retrieve data from the API.'})
    else:
        # If GET req
        form = ItineraryGeneratorForm()

    return render(request, 'itinerary_generator.html', {'form': form})


@login_required
def saved_itineraries(request):
    itineraries = ItineraryGenerator.objects.filter(user=request.user)
    return render(request, 'saved_itineraries.html', {'itineraries': itineraries})

@login_required
def itinerary_detail(request, itinerary_id):
    itinerary = get_object_or_404(ItineraryGenerator, pk=itinerary_id)

    if request.user == itinerary.user:
        return render(request, 'itinerary_detail.html', {'itinerary': itinerary})
    else:
        messages.error(request, "Nice try, go fix your code!.")
        return redirect('saved_itineraries')



@login_required
def delete_itinerary(request, itinerary_id):
    itinerary = get_object_or_404(ItineraryGenerator, pk=itinerary_id)

    if request.method == 'POST':
    # Checks if the user has the itinerary
        if request.user == itinerary.user:
            itinerary.delete()
            messages.success(request, 'Your itinerary has been deleted!')
        else:
            messages.error(request, 'The itinerary cannot be deleted.')
            pass

        return redirect('saved_itineraries')

    # Rendering a confirmation page if GET request
    return redirect('confirm_itinerary_deletion', itinerary_id=itinerary_id)


@login_required
def confirm_itinerary_deletion(request, itinerary_id):
    itinerary = get_object_or_404(ItineraryGenerator, pk=itinerary_id)

    return render(request, 'confirm_itinerary_deletion.html', {'itinerary': itinerary})
