import re
from rest_framework import serializers
from .models import Donor

class DonorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donor
        fields = [
            'id',
            'full_name',
            'age',
            'gender',
            'blood_group',
            'phone',
            'email',
            'city',
            'address',
            'last_donation_date',
            'availability',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_full_name(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("Full Name is required and cannot be empty.")
        if len(value.strip()) < 3:
            raise serializers.ValidationError("Full Name must have at least 3 characters.")
        return value.strip()

    def validate_age(self, value):
        if value < 18 or value > 65:
            raise serializers.ValidationError("Age must be between 18 and 65 years for blood donation eligibility.")
        return value

    def validate_blood_group(self, value):
        valid_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        if value not in valid_groups:
            raise serializers.ValidationError(f"Invalid blood group '{value}'. Valid choices: {', '.join(valid_groups)}.")
        return value

    def validate_phone(self, value):
        phone_clean = value.strip()
        pattern = r'^\+?[0-9]{10,15}$'
        if not re.match(pattern, phone_clean):
            raise serializers.ValidationError("Phone number must contain between 10 and 15 digits (e.g., 9876543210 or +919876543210).")
        return phone_clean

    def validate_city(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("City is required and cannot be empty.")
        return value.strip()

    def validate_availability(self, value):
        if value not in ['Available', 'Unavailable']:
            raise serializers.ValidationError("Availability must be either 'Available' or 'Unavailable'.")
        return value
