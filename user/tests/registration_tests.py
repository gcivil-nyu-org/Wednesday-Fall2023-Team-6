from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.messages import get_messages, constants
from user.models import Patient, Choices
from doctor.models import Doctor
from hospital.models import HospitalAdmin, Hospital

from MediLink.settings import MESSAGE_TAGS

class RegistrationTests(TestCase):
    
    @classmethod
    def setUpClass(self):
        #Create Patient
        self.patient_user_email = "test_patient_user@gmail.com"
        self.user_password = "test_password"
        
        #Create Doctor
        self.doctor_user_email = "test_doctor_user@gmail.com"
        
        #Create Hospital Admin
        self.admin_user_email = "test_admin_user@gmail.com"
        
        self.hosiptal = Hospital.objects.create(name="Test", facility_type="Test", borough="Test", phone="34536", location="Test", postal_code=12345)
    
    def test_nonexisting_user(self):
        print("\nRunning: test for checking registration of nonexisting user")
        post_data_patient = {
            "user_email": self.patient_user_email,
            "user_name": self.user_password,
            "user_sex": "male",
            "user_phone": "5002001000",
            "userType": "patient",
            "user_address": "73rd Street",
            "borough": "BKN",
            "zip_code": 11209,
            "insurance": "NYU Insurance"
        }
        
        post_data_doctor = {
            "user_email": self.doctor_user_email,
            "user_name": self.user_password,
            "user_sex": "male",
            "user_phone": "5002001000",
            "userType": "doctor",
            "user_address": "73rd Street",
            "borough": "BKN",
            "zip_code": 11209,
            "specialization": "Pediatrician",
            "hospital": None,  
        }
        
        post_data_hospital = {
            "user_email": self.admin_user_email,
            "user_name": self.user_password,
            "user_sex": "male",
            "user_phone": "5002001000",
            "userType": "hospital-admin",
            "user_address": "73rd Street",
            "borough": "BKN",
            "zip_code": 11209,
            "hospital": self.hosiptal.id,  
        }
        
        post_data_users = [post_data_patient, post_data_doctor, post_data_hospital]
        
        for post_data in post_data_users:
            response = self.client.post('/user/registration/', post_data)
            if post_data["userType"] == 'patient':
                self.assertTrue(Patient.objects.filter(email=post_data["user_email"]).exists())
                user = Patient.objects.get(email=post_data["user_email"])
            elif post_data["userType"] == 'doctor':
                self.assertTrue(Doctor.objects.filter(email=post_data["user_email"]).exists())
                user = Doctor.objects.get(email=post_data["user_email"])
            else:
                self.assertTrue(HospitalAdmin.objects.filter(email=post_data["user_email"]).exists())
                user = HospitalAdmin.objects.get(email=post_data["user_email"])            

            self.assertEqual(user.name, post_data["user_name"])
            self.assertEqual(user.sex.lower(), str(post_data["user_sex"]).lower())
            self.assertEqual(user.phone, post_data["user_phone"])
            
            borough_converter = {}
            for bor in Choices.boroughs:
                borough_converter[bor[0]] = bor[1]
            self.assertEqual(user.borough, borough_converter[post_data["borough"]])
            self.assertEqual(user.address, post_data["user_address"])
            self.assertEqual(user.zip, post_data["zip_code"])
            self.assertEqual(user.insurance_provider, post_data["insurance"])
            
            logged_in_user = auth.get_user(self.client)
            self.assertEqual(logged_in_user.get_username(), post_data["user_email"]) 
            self.assertTrue(logged_in_user.is_authenticated)
            self.assertRedirects(
                response=response,
                expected_url="/user/home/",
                status_code=302,
                target_status_code=200
            )   
            self.client.logout()     
        
        #Replace with our logout call later
        print("Completed: test for checking login of nonexisting user")
    
    def test_existing_user_all_data(self):
        print("\nRunning: test for checking registration of existing users")
        post_data_patient = {
            "user_email": self.patient_user_email,
            "user_name": "Patient",
            "password": self.user_password,
            "user_sex": "male",
            "user_phone": "5002001000",
            "userType": "patient",
            "user_address": "73rd Street",
            "borough": "BKN",
            "zip_code": 11209,
            "insurance": "NYU Insurance"
        }
        
        post_data_doctor = {
            "user_email": self.doctor_user_email,
            "user_name": "Doctor",
            "password": self.user_password,
            "user_sex": "male",
            "user_phone": "5002001000",
            "userType": "doctor",
            "user_address": "73rd Street",
            "borough": "BKN",
            "zip_code": 11209,
            "specialization": "Pediatrician",
            "hospital": None,  
        }
        
        post_data_hospital = {
            "user_email": self.admin_user_email,
            "user_name": "Hospital",
            "password": self.user_password,
            "user_sex": "male",
            "user_phone": "5002001000",
            "userType": "hospital-admin",
            "user_address": "73rd Street",
            "borough": "BKN",
            "zip_code": 11209,
            "hospital": self.hosiptal.id,  
        }
        
        post_data_users = [post_data_patient, post_data_doctor, post_data_hospital]
        
        for post_data in post_data_users:
            response = self.client.post('/user/registration/', post_data)
            if post_data["userType"] == 'patient':
                self.assertFalse(Patient.objects.filter(email=post_data["user_email"]).exists())
            elif post_data["userType"] == 'doctor':
                self.assertFalse(Doctor.objects.filter(email=post_data["user_email"]).exists())
            else:
                self.assertFalse(HospitalAdmin.objects.filter(email=post_data["user_email"]).exists())
            self.assertFalse(User.objects.filter(email=post_data["user_email"]).exists())            
            logged_in_user = auth.get_user(self.client)
            self.assertNotEqual(logged_in_user.get_username(), self.patient_user_email) 
            self.assertFalse(logged_in_user.is_authenticated)
            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0].tags, MESSAGE_TAGS[constants.ERROR])
            self.assertRedirects(
                response=response,
                expected_url="/user/registration/",
                status_code=302,
                target_status_code=200
            )     
        
        #Replace with our logout call later
        print("Completed: test for checking registration of existing users")
    
    def test_nonexisting_user_incorrect_data(self):
        print("\nRunning: test for checking registration of incorrect users")
        post_invalid_email = {
            "user_email": "invalid",
            "user_name": "Name LName",
            "password": self.user_password,
            "user_sex": "male",
            "user_phone": "1234567890",
            "userType": "patient",
            "user_address": "73rd Street",
            "borough": "BKN",
            "zip_code": 11209,
        }
        
        post_invalid_name = {
            "user_email": "valid@gmail.com",
            "user_name": "",
            "password": self.user_password,
            "user_sex": "male",
            "user_phone": "1234567890",
            "userType": "patient",
            "user_address": "73rd Street",
            "borough": "BKN",
            "zip_code": 11209,
        }
        
        post_invalid_password = {
            "user_email": "valid@gmail.com",
            "user_name": "Name LName",
            "password": "",
            "user_sex": "male",
            "user_phone": "1234567890",
            "userType": "patient",
            "user_address": "73rd Street",
            "borough": "BKN",
            "zip_code": 11209,
        }
        
        post_invalid_sex = {
            "user_email": "valid@gmail.com",
            "user_name": "Name LName",
            "password": self.user_password,
            "user_sex": "gmale",
            "user_phone": "1234567890",
            "userType": "patient",
            "user_address": "73rd Street",
            "borough": "BKN",
            "zip_code": 11209,
        }
        
        post_invalid_phone = {
            "user_email": "valid@gmail.com",
            "user_name": "Name LName",
            "password": self.user_password,
            "user_sex": "male",
            "user_phone": "0",
            "userType": "patient",
            "user_address": "73rd Street",
            "borough": "BKN",
            "zip_code": 11209,
        }    
        
        post_invalid_type = {
            "user_email": "valid@gmail.com",
            "user_name": "Name LName",
            "password": self.user_password,
            "user_sex": "male",
            "user_phone": "1234567890",
            "userType": "none",
            "user_address": "73rd Street",
            "borough": "BKN",
            "zip_code": 11209,
        }   
        
        post_invalid_borough = {
            "user_email": "valid@gmail.com",
            "user_name": "Name LName",
            "password": self.user_password,
            "user_sex": "male",
            "user_phone": "1234567890",
            "userType": "patient",
            "user_address": "73rd Street",
            "borough": "Brooklyn",
            "zip_code": 11209,
            "specialization": "Pediatrician",
        }    
        
        post_invalid_hospital = {
            "user_email": "valid@gmail.com",
            "user_name": "Name LName",
            "password": self.user_password,
            "user_sex": "male",
            "user_phone": "1234567890",
            "userType": "hospital-admin",
            "user_address": "73rd Street",
            "borough": "Brooklyn",
            "zip_code": 11209,
            "hospital": None,
        }  
        
        post_data_users = [post_invalid_email, post_invalid_name, post_invalid_password, post_invalid_sex, post_invalid_phone, post_invalid_type, post_invalid_borough, post_invalid_hospital]
        
        for post_data in post_data_users:
            response = self.client.post('/user/registration/', post_data)
            if post_data["userType"] == 'patient':
                self.assertFalse(Patient.objects.filter(email=post_data["user_email"]).exists())
            elif post_data["userType"] == 'doctor':
                self.assertFalse(Doctor.objects.filter(email=post_data["user_email"]).exists())
            else:
                self.assertFalse(HospitalAdmin.objects.filter(email=post_data["user_email"]).exists())
            self.assertFalse(User.objects.filter(email=post_data["user_email"]).exists())            
            logged_in_user = auth.get_user(self.client)
            self.assertNotEqual(logged_in_user.get_username(), self.patient_user_email) 
            self.assertFalse(logged_in_user.is_authenticated)
            messages = list(get_messages(response.wsgi_request))
            self.assertEqual(len(messages), 1)
            self.assertEqual(messages[0].tags, MESSAGE_TAGS[constants.ERROR])
            self.assertRedirects(
                response=response,
                expected_url="/user/registration/",
                status_code=302,
                target_status_code=200
            )     
        
        #Replace with our logout call later
        print("Completed: test for checking registration of incorrect users")
    
    def tearDown(self):
        self.client.logout()
    
    @classmethod
    def tearDownClass(self):
        User.objects.get(username=self.patient_user_email).delete()
        User.objects.get(username=self.doctor_user_email).delete()
        User.objects.get(username=self.doctor_user_email).delete()
