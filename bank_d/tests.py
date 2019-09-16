from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings

from .models import Banks, Branches
## Banks
# name = models.CharField(max_length=49)
# bankid = models.BigIntegerField(primary_key=True)

## Branches
# ifsc = models.CharField(max_length=11, primary_key=True)
# bank = models.ForeignKey(Banks, on_delete=models.CASCADE)
# branch = models.CharField(max_length=74) 
# address = models.TextField()
# city = models.CharField(max_length=80) ## This is giving the error if the length is 50
# district = models.CharField(max_length=50)
# state = models.CharField(max_length=26)

User = get_user_model()
payload_handler =api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

class bankIFSCTestCase(APITestCase):
	def setUp(self):
		user = User(username='test', email='test@test.com')
		user.set_password("something")
		user.save()

		bank_obj = Banks.objects.create(
					name = "bank",
					bankid = 999
				)
		branch_obj = Branches.objects.create(
					ifsc = "123abc",
					branch = "branch",
					address = "address",
					city = "city",
					district = "district",
					state = "state",
					bank = bank_obj
				)

	def test_createUser(self):
		user_count = User.objects.count()
		self.assertEqual(user_count,1)

	def test_createBank(self):
		user_count = Branches.objects.count()
		self.assertEqual(user_count,1) 

	def test_get_bank_from_ifsc(self):
		data = {}
		# response = self.client.get(
		# 	"http://localhost:8000/bank_d/ifsc/123abc", 
		# 	data= data, 
		# 	format='json'
		# )
		response = self.client.get(
			"http://127.0.0.1:8000/bank_d/ifsc/ABHY0065001", 
			data= data, 
			format='json'
		)

		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_auth_user(self):
		user 		= User.objects.first()
		payload 	= payload_handler(user)
		token_rsp 	= encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION="JWT "+token_rsp)
		print("token_rsp:", token_rsp)

	def test_jwt(self):
		data = {
			"username": "test",
			"password": "something",
		}
		url = "http://127.0.0.1:8000/api/auth/login/"
		response = self.client.post(url,data)
		print(response.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		token = response.data.get("token")
		if token != None:
			urlIFSC = "http://127.0.0.1:8000/bank_d/ifsc/ABHY0065001"
			header = {'Authorization': ' JWT '+ token}
			response = self.client.get(urlIFSC, data, **header)
			print("response:", response.data)
			self.assertEqual(response.status_code, status.HTTP_200_OK)

			urlBranch = "http://127.0.0.1:8000/bank_d/branches/ABHYUDAYA%20COOPERATIVE%20BANK%20LIMITED/MUMBAI?limit=1"
			response = self.client.get(urlBranch, data, **header)
			# print("response:", response)
			self.assertEqual(response.status_code, status.HTTP_200_OK)


