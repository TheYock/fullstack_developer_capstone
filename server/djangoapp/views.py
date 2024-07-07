# Uncomment the required imports before adding the code

from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from datetime import datetime

from django.http import JsonResponse
from django.contrib.auth import login, authenticate
import logging
import json
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel  # Ensure this line is present
from .populate import initiate  # Ensure this line is present
from .restapis import get_request, analyze_review_sentiments, post_review
# from .populate import initiate


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create a `login_request` view to handle sign in request
@csrf_exempt
def login_user(request):
    # Get username and password from request.POST dictionary
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    # Try to check if provide credential can be authenticated
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    if user is not None:
        # If user is valid, call login method to login current user
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
    return JsonResponse(data)

# Create a `logout_request` view to handle sign out request
def logout_user(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)

# Create a `registration` view to handle sign up request
# @csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data['userName']
        password = data['password']
        first_name = data['firstName']
        last_name = data['lastName']
        email = data['email']
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Already Registered"})
        
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
        login(request, user)
        
        return JsonResponse({"userName": username, "status": "Registered"})
    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)

def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if count == 0:
        initiate()
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car_model in car_models:
        cars.append({"CarModel": car_model.name, "CarMake": car_model.car_make.name})
    return JsonResponse({"CarModels": cars})
# # Update the `get_dealerships` view to render the index page with
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = f"/fetchDealers/{state}"
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "dealers": dealerships})

# Create a `get_dealer_details` view to render the dealer details
def get_dealer_details(request, dealer_id):
    endpoint = f"/fetchDealer/{dealer_id}"
    dealer_details = get_request(endpoint)
    return JsonResponse({"status": 200, "dealer_details": dealer_details})

# Create a `get_dealer_reviews` view to render the reviews of a dealer
def get_dealer_reviews(request, dealer_id):
    endpoint = f"/fetchReviews/dealer/{dealer_id}"
    reviews = get_request(endpoint)
    
    for review in reviews:
        sentiment = analyze_review_sentiments(review['review'])
        review['sentiment'] = sentiment['label']  # Assuming sentiment analysis returns a label field
    
    return JsonResponse({"status": 200, "dealer_reviews": reviews})

def add_review(request):
    if request.user.is_authenticated:
        data = json.loads(request.body)
        try:
            response = post_review(data)
            return JsonResponse({"status": 200, "response": response})
        except Exception as err:
            return JsonResponse({"status": 401, "message": str(err)})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
