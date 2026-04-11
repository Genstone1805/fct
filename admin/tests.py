from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from account.models import UserProfile
from .models import Leads


@override_settings(API_KEY="test-api-key")
class LeadEndpointsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = UserProfile.objects.create_superuser(
            email="admin@example.com",
            password="password123"
        )
        self.api_key_headers = {"HTTP_API_KEY": "test-api-key"}
        self.lead = Leads.objects.create(name="Jane Doe", email="jane@example.com")

    def test_create_lead_with_api_key(self):
        response = self.client.post(
            reverse("admin-lead-create"),
            {"name": "John Doe", "email": "john@example.com"},
            format="json",
            **self.api_key_headers,
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()["message"], "Lead created successfully")
        self.assertTrue(Leads.objects.filter(email="john@example.com").exists())

    def test_list_leads_requires_admin_user(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get(
            reverse("admin-lead-list"),
            **self.api_key_headers,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json()[0]["email"], self.lead.email)

    def test_retrieve_lead_requires_admin_user(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.get(
            reverse("admin-lead-detail", args=[self.lead.pk]),
            **self.api_key_headers,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()["name"], self.lead.name)
        self.assertEqual(response.json()["email"], self.lead.email)

    def test_delete_lead_requires_admin_user(self):
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.delete(
            reverse("admin-lead-delete", args=[self.lead.pk]),
            **self.api_key_headers,
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Leads.objects.filter(pk=self.lead.pk).exists())
