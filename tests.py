from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Donor

class DonorAPITests(APITestCase):
    def setUp(self):
        self.donor1 = Donor.objects.create(
            full_name="Manoj Tiwari",
            age=30,
            gender="Male",
            blood_group="O+",
            phone="9876543210",
            email="manoj@example.com",
            city="Chennai",
            address="10 Marina Beach Rd",
            availability="Available"
        )
        self.donor2 = Donor.objects.create(
            full_name="Anita Roy",
            age=25,
            gender="Female",
            blood_group="A-",
            phone="9876543211",
            email="anita@example.com",
            city="Bengaluru",
            address="50 Whitefield",
            availability="Unavailable"
        )

    # 1. Create valid donor
    def test_create_valid_donor(self):
        url = reverse('api_donor_list_create')
        data = {
            "full_name": "Suresh Raina",
            "age": 34,
            "gender": "Male",
            "blood_group": "B+",
            "phone": "9876543212",
            "email": "suresh@example.com",
            "city": "Chennai",
            "address": "20 Mount Road",
            "availability": "Available"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['data']['full_name'], "Suresh Raina")

    # 2. Create donor with missing data
    def test_create_donor_missing_fields(self):
        url = reverse('api_donor_list_create')
        data = {
            "full_name": "Incomplete Donor"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')

    # 3. Invalid email test
    def test_create_donor_invalid_email(self):
        url = reverse('api_donor_list_create')
        data = {
            "full_name": "Invalid Email Donor",
            "age": 28,
            "gender": "Male",
            "blood_group": "AB+",
            "phone": "9876543213",
            "email": "not-an-email",
            "city": "Delhi",
            "address": "12 Connaught Place",
            "availability": "Available"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data['errors'])

    # 4. Invalid age test (underage < 18)
    def test_create_donor_underage(self):
        url = reverse('api_donor_list_create')
        data = {
            "full_name": "Too Young",
            "age": 15,
            "gender": "Male",
            "blood_group": "O+",
            "phone": "9876543214",
            "email": "young@example.com",
            "city": "Mumbai",
            "address": "1 Marine Lines",
            "availability": "Available"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('age', response.data['errors'])

    # 5. Read all donors
    def test_read_all_donors(self):
        url = reverse('api_donor_list_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertGreaterEqual(response.data['count'], 2)

    # 6. Read one donor
    def test_read_single_donor(self):
        url = reverse('api_donor_detail', kwargs={'pk': self.donor1.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['full_name'], self.donor1.full_name)

    # 7. Update donor
    def test_update_donor(self):
        url = reverse('api_donor_detail', kwargs={'pk': self.donor1.id})
        updated_data = {
            "city": "Madurai",
            "availability": "Unavailable"
        }
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['city'], "Madurai")
        self.assertEqual(response.data['data']['availability'], "Unavailable")

    # 8. Invalid donor ID
    def test_read_invalid_donor_id(self):
        url = reverse('api_donor_detail', kwargs={'pk': 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['status'], 'error')

    # 9. Delete donor
    def test_delete_donor(self):
        url = reverse('api_donor_detail', kwargs={'pk': self.donor2.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Donor.objects.filter(pk=self.donor2.id).exists())

    # 10. Search donor
    def test_search_donor_by_name(self):
        url = reverse('api_donor_list_create') + "?search=Manoj"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['data'][0]['full_name'], "Manoj Tiwari")

    # 11. Filter donor by blood group
    def test_filter_donor_by_blood_group(self):
        url = reverse('api_donor_list_create') + "?blood_group=A-"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for donor in response.data['data']:
            self.assertEqual(donor['blood_group'], 'A-')
