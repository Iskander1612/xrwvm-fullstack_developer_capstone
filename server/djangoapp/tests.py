import json
from unittest.mock import patch
from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import CarMake, CarModel
class ApplicationTests(TestCase):
    def setUp(self):
        self.user=User.objects.create_user(username="driver",password="DemoTest2026!",first_name="Test",last_name="Driver")
    def test_login_rejects_invalid_password(self):
        response=self.client.post("/djangoapp/login",data=json.dumps({"userName":"driver","password":"wrong"}),content_type="application/json")
        self.assertEqual(response.status_code,401)
    def test_login_and_logout_session(self):
        self.client.post("/djangoapp/login",data=json.dumps({"userName":"driver","password":"DemoTest2026!"}),content_type="application/json")
        self.assertEqual(self.client.get("/djangoapp/session").json()["userName"],"driver")
        self.assertEqual(self.client.post("/djangoapp/logout").status_code,200)
        self.assertIsNone(self.client.get("/djangoapp/session").json()["userName"])
    def test_registration_and_duplicate(self):
        data={"userName":"newdriver","password":"GreatTest2026!","firstName":"New","lastName":"Driver","email":"new@example.com"}
        self.assertEqual(self.client.post("/djangoapp/register",json.dumps(data),content_type="application/json").status_code,201)
        self.assertEqual(self.client.post("/djangoapp/register",json.dumps(data),content_type="application/json").status_code,409)
    def test_post_review_requires_login(self):
        self.assertEqual(self.client.post("/djangoapp/add_review",'{}',content_type="application/json").status_code,401)
    @patch("djangoapp.views.post_review",return_value={"id":99})
    @patch("djangoapp.views.get_request",return_value=[{"id":1}])
    def test_review_uses_authenticated_name(self,get,post):
        self.client.force_login(self.user)
        data={"dealership":1,"review":"Great service","car_year":2023,"name":"Spoofed name"}
        response=self.client.post("/djangoapp/add_review",json.dumps(data),content_type="application/json")
        self.assertEqual(response.status_code,201)
        self.assertEqual(post.call_args.args[0]["name"],"Test Driver")
    @patch("djangoapp.views.get_request",return_value=[{"id":5,"state":"Kansas"}])
    def test_state_filter_routes_correctly(self,get):
        response=self.client.get("/djangoapp/get_dealers/Kansas")
        self.assertEqual(response.json()["dealers"][0]["state"],"Kansas")
        get.assert_called_once_with("fetchDealers/Kansas")
    def test_catalog_serialization(self):
        make=CarMake.objects.create(name="Nissan")
        CarModel.objects.create(car_make=make,name="Pathfinder",type="SUV",year=2023)
        self.assertEqual(self.client.get("/djangoapp/get_cars").json()["CarModels"][0]["CarMake"],"Nissan")
    def test_csrf_required_for_login(self):
        client=Client(enforce_csrf_checks=True)
        self.assertEqual(client.post("/djangoapp/login",'{}',content_type="application/json").status_code,403)
    def test_static_pages(self):
        for url,title in [("/about","About Best Cars"),("/contact","Contact Us")]:
            self.assertContains(self.client.get(url),title)
