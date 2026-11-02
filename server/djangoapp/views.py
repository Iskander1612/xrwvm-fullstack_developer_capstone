import json
import logging
from functools import wraps
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST, require_GET
import requests
from .models import CarMake, CarModel
from .restapis import get_request, post_review, analyze_review_sentiments
logger = logging.getLogger(__name__)

def service_errors(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        try: return view(*args, **kwargs)
        except requests.RequestException:
            logger.exception("Upstream service unavailable")
            return JsonResponse({"status": 503, "error": "A service is temporarily unavailable. Please try again."}, status=503)
        except (ValueError, KeyError, TypeError):
            return JsonResponse({"status": 400, "error": "Invalid request data"}, status=400)
    return wrapped

@ensure_csrf_cookie
def index(request, path=""):
    return render(request, "index.html")
@ensure_csrf_cookie
def about(request): return render(request, "About.html")
@ensure_csrf_cookie
def contact(request): return render(request, "Contact.html")
@require_GET
def session(request):
    return JsonResponse({"userName": request.user.username if request.user.is_authenticated else None})
@require_POST
@service_errors
def login_user(request):
    data = json.loads(request.body)
    user = authenticate(request, username=data.get("userName", ""), password=data.get("password", ""))
    if user is None: return JsonResponse({"status": "Invalid credentials"}, status=401)
    login(request, user)
    return JsonResponse({"userName": user.username, "firstName": user.first_name, "lastName": user.last_name, "status": "Authenticated"})
@require_POST
def logout_request(request):
    logout(request)
    return JsonResponse({"status": "Logged out"})
@require_POST
@service_errors
def registration(request):
    data = json.loads(request.body)
    username = data.get("userName", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    if not username or len(username)>150 or not data.get("firstName") or not data.get("lastName"):
        return JsonResponse({"error": "All five fields are required"}, status=400)
    if User.objects.filter(username=username).exists(): return JsonResponse({"error": "Username already exists"}, status=409)
    try:
        validate_email(email)
        validate_password(password)
    except ValidationError as error:
        return JsonResponse({"error": " ".join(error.messages)}, status=400)
    user = User.objects.create_user(username=username, email=email, password=password, first_name=data["firstName"], last_name=data["lastName"])
    login(request, user)
    return JsonResponse({"status": "Authenticated", "userName": username}, status=201)
@require_GET
@service_errors
def get_dealerships(request, state="All"):
    endpoint = "fetchDealers" if state == "All" else f"fetchDealers/{state}"
    return JsonResponse({"status": 200, "dealers": get_request(endpoint)})
@require_GET
@service_errors
def get_dealer_details(request, dealer_id):
    dealer = get_request(f"fetchDealer/{dealer_id}")
    return JsonResponse({"status": 200 if dealer else 404, "dealer": dealer}, status=200 if dealer else 404)
@require_GET
@service_errors
def get_dealer_reviews(request, dealer_id):
    reviews = get_request(f"fetchReviews/dealer/{dealer_id}")
    for review in reviews:
        review["sentiment"] = analyze_review_sentiments(review["review"])["sentiment"]
    return JsonResponse({"status": 200, "reviews": reviews})
@require_GET
def get_cars(request):
    makes = list(CarMake.objects.values("id", "name", "description"))
    models = [{"id": x.id, "CarMake": x.car_make.name, "CarModel": x.name, "year": x.year, "type": x.type} for x in CarModel.objects.select_related("car_make").all()]
    return JsonResponse({"status": 200, "CarMakes": makes, "CarModels": models})
@require_POST
@service_errors
def add_review(request):
    if not request.user.is_authenticated: return JsonResponse({"error": "Please log in to review a dealer"}, status=401)
    data = json.loads(request.body)
    if not str(data.get("review", "")).strip(): return JsonResponse({"error": "Review is required"}, status=400)
    data["dealership"] = int(data["dealership"])
    data["car_year"] = int(data["car_year"])
    if not 2015 <= data["car_year"] <= 2026: return JsonResponse({"error": "Choose a year between 2015 and 2026"}, status=400)
    if not get_request(f'fetchDealer/{data["dealership"]}'): return JsonResponse({"error": "Dealer not found"}, status=404)
    data["name"] = request.user.get_full_name() or request.user.username
    return JsonResponse({"status": 200, "review": post_review(data)}, status=201)
