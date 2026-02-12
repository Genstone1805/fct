from rest_framework import serializers


class ContactSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    whatsapp_number = serializers.CharField(max_length=20, required=False, allow_blank=True)
    about = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField()
    subject = serializers.CharField(max_length=200)
    message = serializers.CharField()