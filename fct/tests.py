from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
import json


class ContactUsViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.contact_url = reverse('contact-us')

    def test_contact_us_get_request(self):
        """Test GET request to contact us endpoint"""
        response = self.client.get(self.contact_url)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())
        self.assertIn('fields', response.json())

    @patch('fct.views.send_mail')
    def test_contact_us_post_success(self, mock_send_mail):
        """Test successful contact form submission"""
        # Mock the send_mail function to avoid actual email sending
        mock_send_mail.return_value = 1
        
        data = {
            'name': 'John Doe',
            'whatsapp_number': '+1234567890',
            'about': 'Customer inquiry',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message'
        }
        
        response = self.client.post(
            self.contact_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['message'], 'Contact form submitted successfully')
        # Verify that send_mail was called
        mock_send_mail.assert_called_once()

    def test_contact_us_post_missing_fields(self):
        """Test contact form submission with missing required fields"""
        # Test missing name
        data = {
            'whatsapp_number': '+1234567890',
            'about': 'Customer inquiry',
            'email': 'john@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message'
        }
        
        response = self.client.post(
            self.contact_url,
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())

    def test_contact_us_post_invalid_json(self):
        """Test contact form submission with invalid JSON"""
        response = self.client.post(
            self.contact_url,
            data='invalid json',
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.json())