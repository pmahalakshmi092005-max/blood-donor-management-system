# Blood Donor Availability Management System 🩸

A full-stack, CRUD-based web application developed using **Python, Django, Django REST Framework, SQLite, HTML5, CSS3, and Bootstrap 5**.

The system enables hospitals, blood banks, and patients in emergency need to search, identify, register, and manage available blood donors based on blood group and location.

---

## 1. Project Overview & Problem Statement
In emergency healthcare situations (such as trauma cases, surgeries, and critical transfusions), finding compatible blood donors quickly is often a matter of life and death. Traditional phone trees or informal messaging are slow and error-prone.

The **Blood Donor Availability Management System** solves this by providing:
- Instant multi-parameter search (by blood group, city, phone number, and name).
- Real-time donor availability tracking (Available vs. Unavailable).
- Complete CRUD operations (Create, Read, Update, Delete) with validation.
- Standardized REST APIs for easy expansion to mobile apps or hospital portals.

---

## 2. Key Features
- **Landing Page (Home):** Hero banner, live donor statistics counter, and "Why Donate Blood" information cards.
- **Analytics Dashboard:** Real-time distribution across all 8 blood groups (`A+`, `A-`, `B+`, `B-`, `AB+`, `AB-`, `O+`, `O-`), availability counts, and recent donor registrations.
- **Donor Directory (Read):** Clean, searchable, and filterable table with color-coded availability badges.
- **Donor Registration (Create):** Comprehensive form with both frontend and backend validation for age (18-65), phone numbers, and email formats.
- **Donor Profile (Detail):** Detailed profile view with donor contact details and one-click direct dialing.
- **Donor Edit (Update):** Edit existing records with pre-filled fields and update validation.
- **Donor Removal (Delete):** Safety confirmation dialog before permanently removing records.
- **RESTful API:** Clean JSON endpoints supporting GET, POST, PUT, and DELETE operations with standard HTTP status codes.
- **Django Administration:** Secure admin panel (`/admin/`) with advanced search and filters.

---

## 3. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | HTML5, CSS3, JavaScript, Bootstrap 5.3, Bootstrap Icons | Responsive UI, form validation, and modern healthcare theme |
| **Backend** | Python 3.13, Django 6.1 | Model-View-Template (MVT) web framework |
| **API** | Django REST Framework (DRF) | RESTful JSON API endpoints |
| **Database** | SQLite 3 | Embedded relational database |
| **Testing** | Django APITestCase & Unit Tests, Postman | Automated backend testing and API contract verification |
| **Version Control** | Git & GitHub | Source code tracking |

---

## 4. Project Directory Structure

```text
blood_donor_system/
│
├── manage.py                     # Django management script
├── db.sqlite3                    # SQLite database file
├── requirements.txt              # Project dependencies
├── README.md                     # Documentation & setup guide
├── .gitignore                    # Ignored files for Git
│
├── blood_donor_system/           # Main project configuration
│   ├── __init__.py
│   ├── settings.py               # Django configuration & installed apps
│   ├── urls.py                   # Master URL routing
│   ├── asgi.py
│   └── wsgi.py
│
├── donors/                       # Blood Donor Application
│   ├── migrations/               # Database migration files
│   ├── __init__.py
│   ├── admin.py                  # Django admin registration
│   ├── apps.py                   # App configuration
│   ├── models.py                 # Donor database model & schema
│   ├── serializers.py            # DRF Serializers for JSON validation
│   ├── forms.py                  # Django Forms with validation
│   ├── views.py                  # Web Views & REST API View classes
│   ├── urls.py                   # Donor app URL routes
│   └── tests.py                  # 11 Automated unit & API tests
│
├── templates/                    # HTML5 Templates
│   ├── base.html                 # Master layout (navbar, alerts, footer)
│   ├── index.html                # Home / Landing page
│   ├── dashboard.html            # Analytics dashboard & blood group stats
│   ├── donor_list.html           # Donors table with search & filter
│   ├── donor_form.html           # Donor registration & edit form
│   ├── donor_detail.html         # Single donor profile
│   ├── donor_confirm_delete.html # Delete confirmation modal
│   ├── about.html                # Blood compatibility matrix & about
│   └── 404.html                  # Custom 404 page
│
└── static/                       # Static Assets
    ├── css/
    │   └── style.css             # Healthcare UI theme & animations
    ├── js/
    │   └── main.js               # Client validation & alert handling
    └── images/                   # Visual assets
```

---

## 5. Installation & Setup Guide

Follow these simple steps in your terminal to set up and run the project locally:

### Step 1: Clone or Navigate to Project
```powershell
cd "C:\Users\ANANDA MOORTHY P\.gemini\antigravity\scratch\blood_donor_system"
```

### Step 2: Create & Activate Virtual Environment
```powershell
# Create virtual environment
python -m venv venv

# Activate on Windows PowerShell
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 4: Apply Database Migrations
```powershell
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Run the Development Server
```powershell
python manage.py runserver
```

Open your web browser and visit:
👉 **http://127.0.0.1:8000/**

---

## 6. Default Credentials
- **Django Admin Panel:** `http://127.0.0.1:8000/admin/`
  - **Username:** `admin`
  - **Password:** `admin123`

---

## 7. REST API Endpoints

| Method | Endpoint | Description | Status Code |
|---|---|---|---|
| `GET` | `/api/donors/` | List all donors (supports query filters) | `200 OK` |
| `POST` | `/api/donors/` | Create a new donor record | `201 Created` / `400 Bad Request` |
| `GET` | `/api/donors/<id>/` | Retrieve details of a specific donor | `200 OK` / `404 Not Found` |
| `PUT` | `/api/donors/<id>/` | Update an existing donor record | `200 OK` / `400 Bad Request` |
| `DELETE` | `/api/donors/<id>/` | Permanently delete a donor | `200 OK` / `404 Not Found` |
| `GET` | `/api/statistics/` | Real-time counts of donors & blood groups | `200 OK` |

### Sample JSON for Adding a Donor (`POST /api/donors/`)
```json
{
  "full_name": "Kavitha Raman",
  "age": 28,
  "gender": "Female",
  "blood_group": "O+",
  "phone": "9876543299",
  "email": "kavitha.r@example.com",
  "city": "Chennai",
  "address": "45 Cathedral Road, Gopalapuram",
  "availability": "Available"
}
```

---

## 8. Running Automated Tests
Run the automated test suite with:
```powershell
python manage.py test donors
```
**Test Results:**
```text
...........
----------------------------------------------------------------------
Ran 11 tests in 0.157s

OK
```

---

## 9. Viva Questions and Answers (Quick Reference)

1. **What is CRUD?**
   CRUD stands for **Create, Read, Update, Delete** — the four primary database operations required by persistent web applications.
2. **What is Django MVT?**
   Django follows **Model-View-Template**:
   - *Model:* Defines the database structure.
   - *View:* Contains business logic and handles requests.
   - *Template:* The HTML user interface presented to the browser.
3. **What is an ORM?**
   Object-Relational Mapping translates Python classes into SQL database tables, allowing developers to query databases using Python instead of raw SQL strings.
4. **What is the role of Django REST Framework (DRF)?**
   DRF serializes complex Django models into standard JSON and handles HTTP requests, authentication, and status codes for API clients.
5. **How are donor validations enforced?**
   Validation is implemented at two levels:
   - *Client-side (JavaScript):* Provides instant feedback to the user before form submission.
   - *Server-side (Django Models & DRF Serializers):* Guarantees data integrity and prevents invalid or malicious input from entering the database.

---

## 10. License & Academic Disclaimer
This mini-project was developed for educational and college mini-project demonstration purposes.
