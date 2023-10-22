from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.messages import get_messages, constants
from user.models import Patient, Choices
from doctor.models import Doctor
from hospital.models import Hospital

from MediLink.settings import MESSAGE_TAGS

class RegistrationTests(TestCase):
    
    @classmethod
    def setUpClass(self):
        #Create Patient
        self.patient_user_email = "test_patient_user@gmail.com"
        self.user_password = "test_password"
        User.objects.create_user(self.patient_user_email, self.patient_user_email, self.user_password)
        
        #Create Doctor
        self.doctor_user_email = "test_doctor_user@gmail.com"
        User.objects.create_user(self.doctor_user_email, self.doctor_user_email, self.user_password)
        
        #Create Hospital Admin
        self.admin_user_email = "test_admin_user@gmail.com"
        User.objects.create_user(self.admin_user_email, self.admin_user_email, self.user_password)
    
    def test_existing_user_all_data(self):
        print("\nRunning: test for checking registration of existing patient")
        post_data_patient = {
            "user_email": self.patient_user_email,
            "user_name": self.user_password,
            "user_sex": "male",
            "user_phone": "5002001000",
            "userType": "patient",
            "user_address": "73rd Street",
            "borough": "Brooklyn",
            "zip_code": 11209,
            "insurance": "NYU Insurance"
        }
        
        response = self.client.post('/user/registration/', post_data_patient)
        logged_in_user = auth.get_user(self.client)
        self.assertEqual(logged_in_user.get_username(), self.user_email)
        self.assertEqual(Patient.objects.filter(email=post_data_patient["user_email"]).exists())
        user = Patient.objects.get(email=post_data_patient["user_email"])

        self.assertEqual(user.name, post_data_patient["user_name"])
        self.assertEqual(user.sex.lower(), str(post_data_patient["user_name"]).lower())
        self.assertEqual(user.phone, post_data_patient["user_name"])
        
        borough_converter = {}
        for bor in Choices.boroughs:
            borough_converter[bor[0]] = bor[1]
        self.assertEqual(user.borough, borough_converter[post_data_patient["borough"]])
        self.assertEqual(user.address, post_data_patient["user_name"])
        self.assertEqual(user.zip, post_data_patient["user_name"])
        self.assertEqual(user.insurance_provider, post_data_patient["user_name"])
            
        self.assertTrue(logged_in_user.is_authenticated)
        self.assertRedirects(
            response=response,
            expected_url="/user/home/",
            status_code=302,
            target_status_code=200
        )
        
        post_data_doctor = {
            "user_email": self.patient_user_email,
            "user_name": self.user_password,
            "user_sex": "male",
            "user_phone": "5002001000",
            "userType": "patient",
            "user_address": "73rd Street",
            "borough": "Brooklyn",
            "zip_code": 11209,
            "specialization": "Pediatrician",
            "hospital": None,  
        }
        
        post_data_hospital = {
            "user_email": self.patient_user_email,
            "user_name": self.user_password,
            "user_sex": "male",
            "user_phone": "5002001000",
            "userType": "patient",
            "user_address": "73rd Street",
            "borough": "Brooklyn",
            "zip_code": 11209,
            "hospital": 1,  
        }
        
        
        #Replace with our logout call later
        print("Completed: test for checking login of existing user")
    
    def test_existing_user_mandatory_data(self):
        pass
    
    def test_existing_user_wrong_password(self):
        pass
    
    def test_existing_user_incorrect_data(self):
        pass
    
    def test_nonexisting_user(self):
        print("\nRunning: test for checking login of nonexisting user")
        post_data = {
            "user_email": "invalid_email",
            "user_pwd": "invalid_password"
        }
        response = self.client.post('/user/login/', post_data)
        logged_in_user = auth.get_user(self.client)
        self.assertFalse(logged_in_user.is_authenticated)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].tags, MESSAGE_TAGS[constants.ERROR])
        self.assertNotEqual(logged_in_user.get_username(), "invalid_email")
        
        self.assertRedirects(
            response=response,
            expected_url="/user/login/",
            status_code=302,
            target_status_code=200
        )
        print("Completed: test for checking login of nonexisting user\n")
    
    def tearDown(self):
        self.client.logout()
    
    @classmethod
    def tearDownClass(self):
        User.objects.get(username=self.patient_user_email).delete()
        User.objects.get(username=self.doctor_user_email).delete()
        User.objects.get(username=self.doctor_user_email).delete()
