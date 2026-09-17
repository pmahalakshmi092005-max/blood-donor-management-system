// ==========================================================================
// Blood Donor Availability Management System - JavaScript
// ==========================================================================

document.addEventListener('DOMContentLoaded', function () {
    // 1. Auto-dismiss alerts after 4 seconds
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 4000);
    });

    // 2. Client-side Form Validation
    const donorForm = document.querySelector('form.needs-validation');
    if (donorForm) {
        donorForm.addEventListener('submit', function (event) {
            let isValid = true;

            // Validate Full Name
            const nameInput = document.getElementById('id_full_name');
            if (nameInput && nameInput.value.trim().length < 3) {
                isValid = false;
                showFieldError(nameInput, 'Please enter a valid full name (at least 3 characters).');
            } else if (nameInput) {
                clearFieldError(nameInput);
            }

            // Validate Age (18 to 65)
            const ageInput = document.getElementById('id_age');
            if (ageInput) {
                const ageVal = parseInt(ageInput.value, 10);
                if (isNaN(ageVal) || ageVal < 18 || ageVal > 65) {
                    isValid = false;
                    showFieldError(ageInput, 'Eligible blood donor age must be between 18 and 65.');
                } else {
                    clearFieldError(ageInput);
                }
            }

            // Validate Phone (10 to 15 digits)
            const phoneInput = document.getElementById('id_phone');
            if (phoneInput) {
                const phonePattern = /^\+?[0-9]{10,15}$/;
                if (!phonePattern.test(phoneInput.value.trim())) {
                    isValid = false;
                    showFieldError(phoneInput, 'Enter a valid 10-15 digit phone number (e.g. 9876543210).');
                } else {
                    clearFieldError(phoneInput);
                }
            }

            // Validate Email
            const emailInput = document.getElementById('id_email');
            if (emailInput) {
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailPattern.test(emailInput.value.trim())) {
                    isValid = false;
                    showFieldError(emailInput, 'Enter a valid email address.');
                } else {
                    clearFieldError(emailInput);
                }
            }

            // Validate City
            const cityInput = document.getElementById('id_city');
            if (cityInput && cityInput.value.trim() === '') {
                isValid = false;
                showFieldError(cityInput, 'City is required.');
            } else if (cityInput) {
                clearFieldError(cityInput);
            }

            if (!isValid) {
                event.preventDefault();
                event.stopPropagation();
            }
        });
    }

    // Helper functions for field errors
    function showFieldError(input, message) {
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
        let feedback = input.nextElementSibling;
        if (!feedback || !feedback.classList.contains('invalid-feedback')) {
            feedback = document.createElement('div');
            feedback.className = 'invalid-feedback';
            input.parentNode.appendChild(feedback);
        }
        feedback.textContent = message;
    }

    function clearFieldError(input) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    }
});
