from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator

class Donor(models.Model):
    # Blood group options
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ]

    # Availability options
    AVAILABILITY_CHOICES = [
        ('Available', 'Available'),
        ('Unavailable', 'Unavailable'),
    ]

    # Gender options
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]

    # Phone validator (10-15 digits, optional leading +)
    phone_regex = RegexValidator(
        regex=r'^\+?[0-9]{10,15}$',
        message="Phone number must be 10 to 15 digits. Example: 9876543210 or +919876543210."
    )

    # Database fields
    full_name = models.CharField(max_length=100, help_text="Enter donor's full name")
    age = models.PositiveIntegerField(
        validators=[
            MinValueValidator(18, message="Donor must be at least 18 years old."),
            MaxValueValidator(65, message="Donor age must not exceed 65 years.")
        ],
        help_text="Eligible blood donor age is 18 to 65"
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Male')
    blood_group = models.CharField(max_length=5, choices=BLOOD_GROUP_CHOICES)
    phone = models.CharField(validators=[phone_regex], max_length=15, help_text="Contact number")
    email = models.EmailField(help_text="Valid email address")
    city = models.CharField(max_length=100, help_text="Current city")
    address = models.TextField(help_text="Full address details")
    last_donation_date = models.DateField(
        null=True,
        blank=True,
        help_text="Last date of blood donation (optional if first time)"
    )
    availability = models.CharField(
        max_length=15,
        choices=AVAILABILITY_CHOICES,
        default='Available'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Blood Donor'
        verbose_name_plural = 'Blood Donors'

    def __str__(self):
        return f"{self.full_name} ({self.blood_group}) - {self.city} [{self.availability}]"
