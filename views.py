from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q, Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Donor
from .serializers import DonorSerializer
from .forms import DonorForm

# ==============================================================================
# REST API VIEWS (Django REST Framework)
# ==============================================================================

class DonorListCreateAPIView(APIView):
    """
    GET /api/donors/       -> List all donors (supports ?search=, ?blood_group=, ?city=, ?availability=)
    POST /api/donors/      -> Create a new donor record
    """
    def get(self, request):
        donors = Donor.objects.all()

        # Search parameter (name, city, phone)
        search_query = request.GET.get('search') or request.GET.get('q')
        if search_query:
            donors = donors.filter(
                Q(full_name__icontains=search_query) |
                Q(city__icontains=search_query) |
                Q(phone__icontains=search_query)
            )

        # Filter by blood group
        blood_group = request.GET.get('blood_group')
        if blood_group:
            donors = donors.filter(blood_group__iexact=blood_group.strip())

        # Filter by city
        city = request.GET.get('city')
        if city:
            donors = donors.filter(city__icontains=city.strip())

        # Filter by availability
        availability = request.GET.get('availability')
        if availability:
            donors = donors.filter(availability__iexact=availability.strip())

        serializer = DonorSerializer(donors, many=True)
        return Response({
            "status": "success",
            "count": donors.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = DonorSerializer(data=request.data)
        if serializer.is_valid():
            donor = serializer.save()
            return Response({
                "status": "success",
                "message": "Donor registered successfully.",
                "data": DonorSerializer(donor).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "error",
            "message": "Validation failed. Please check the provided data.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


class DonorDetailAPIView(APIView):
    """
    GET /api/donors/<id>/       -> Retrieve single donor details
    PUT/PATCH /api/donors/<id>/ -> Update donor record
    DELETE /api/donors/<id>/    -> Delete donor record
    """
    def get_object(self, pk):
        try:
            return Donor.objects.get(pk=pk)
        except Donor.DoesNotExist:
            return None

    def get(self, request, pk):
        donor = self.get_object(pk)
        if not donor:
            return Response({
                "status": "error",
                "message": f"Donor with ID {pk} does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = DonorSerializer(donor)
        return Response({
            "status": "success",
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    def put(self, request, pk):
        donor = self.get_object(pk)
        if not donor:
            return Response({
                "status": "error",
                "message": f"Donor with ID {pk} does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = DonorSerializer(donor, data=request.data, partial=True)
        if serializer.is_valid():
            updated_donor = serializer.save()
            return Response({
                "status": "success",
                "message": "Donor updated successfully.",
                "data": DonorSerializer(updated_donor).data
            }, status=status.HTTP_200_OK)
        return Response({
            "status": "error",
            "message": "Validation failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    patch = put

    def delete(self, request, pk):
        donor = self.get_object(pk)
        if not donor:
            return Response({
                "status": "error",
                "message": f"Donor with ID {pk} does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        donor_name = donor.full_name
        donor.delete()
        return Response({
            "status": "success",
            "message": f"Donor '{donor_name}' deleted successfully."
        }, status=status.HTTP_200_OK)


class StatisticsAPIView(APIView):
    """
    GET /api/statistics/ -> Live count of donors, availability, and blood group distribution
    """
    def get(self, request):
        total_donors = Donor.objects.count()
        available_donors = Donor.objects.filter(availability='Available').count()
        unavailable_donors = Donor.objects.filter(availability='Unavailable').count()

        blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        group_counts = {}
        for bg in blood_groups:
            group_counts[bg] = Donor.objects.filter(blood_group=bg).count()

        return Response({
            "total_donors": total_donors,
            "available_donors": available_donors,
            "unavailable_donors": unavailable_donors,
            "blood_group_counts": group_counts
        }, status=status.HTTP_200_OK)


# ==============================================================================
# HTML TEMPLATE VIEWS (User Interface)
# ==============================================================================

def home_view(request):
    """Landing page with hero banner, live counters, and 'Why Donate' cards"""
    total_donors = Donor.objects.count()
    available_donors = Donor.objects.filter(availability='Available').count()
    unavailable_donors = Donor.objects.filter(availability='Unavailable').count()
    blood_groups_count = Donor.objects.values('blood_group').distinct().count()

    context = {
        'total_donors': total_donors,
        'available_donors': available_donors,
        'unavailable_donors': unavailable_donors,
        'blood_groups_count': blood_groups_count,
    }
    return render(request, 'index.html', context)


def dashboard_view(request):
    """Analytics dashboard with cards for all 8 blood groups and recent donors"""
    total_donors = Donor.objects.count()
    available_donors = Donor.objects.filter(availability='Available').count()
    unavailable_donors = Donor.objects.filter(availability='Unavailable').count()

    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
    blood_stats = []
    for bg in blood_groups:
        count = Donor.objects.filter(blood_group=bg).count()
        avail_count = Donor.objects.filter(blood_group=bg, availability='Available').count()
        blood_stats.append({
            'group': bg,
            'count': count,
            'available_count': avail_count
        })

    recent_donors = Donor.objects.all().order_by('-created_at')[:8]

    context = {
        'total_donors': total_donors,
        'available_donors': available_donors,
        'unavailable_donors': unavailable_donors,
        'blood_stats': blood_stats,
        'recent_donors': recent_donors,
    }
    return render(request, 'dashboard.html', context)


def donor_list_view(request):
    """Donor records table with search by name/city/phone and filter by group/availability/city"""
    donors = Donor.objects.all()

    # Search query
    q = request.GET.get('q', '').strip()
    if q:
        donors = donors.filter(
            Q(full_name__icontains=q) |
            Q(city__icontains=q) |
            Q(phone__icontains=q) |
            Q(blood_group__icontains=q)
        )

    # Filter by Blood Group
    blood_group = request.GET.get('blood_group', '').strip()
    if blood_group:
        donors = donors.filter(blood_group=blood_group)

    # Filter by City
    city = request.GET.get('city', '').strip()
    if city:
        donors = donors.filter(city__icontains=city)

    # Filter by Availability
    availability = request.GET.get('availability', '').strip()
    if availability:
        donors = donors.filter(availability=availability)

    # Unique list of cities for filter dropdown
    all_cities = Donor.objects.values_list('city', flat=True).distinct().order_by('city')
    blood_groups = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']

    context = {
        'donors': donors,
        'q': q,
        'selected_blood_group': blood_group,
        'selected_city': city,
        'selected_availability': availability,
        'all_cities': all_cities,
        'blood_groups': blood_groups,
        'total_results': donors.count(),
    }
    return render(request, 'donor_list.html', context)


def donor_add_view(request):
    """Add a new donor registration form"""
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            donor = form.save()
            messages.success(request, f"Donor registered successfully. Welcome, {donor.full_name}!")
            return redirect('donor_list')
        else:
            messages.error(request, "Please correct the errors indicated below.")
    else:
        form = DonorForm()

    return render(request, 'donor_form.html', {
        'form': form,
        'title': 'Register New Blood Donor',
        'button_text': 'Save Donor'
    })


def donor_detail_view(request, pk):
    """View single donor profile"""
    donor = get_object_or_404(Donor, pk=pk)
    return render(request, 'donor_detail.html', {'donor': donor})


def donor_edit_view(request, pk):
    """Edit an existing donor's information"""
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        form = DonorForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            messages.success(request, f"Donor updated successfully. Details for {donor.full_name} have been updated.")
            return redirect('donor_list')
        else:
            messages.error(request, "Please check the form for errors.")
    else:
        form = DonorForm(instance=donor)

    return render(request, 'donor_form.html', {
        'form': form,
        'donor': donor,
        'title': f'Edit Donor: {donor.full_name}',
        'button_text': 'Update Donor Details'
    })


def donor_delete_view(request, pk):
    """Confirmation page and deletion action"""
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        donor_name = donor.full_name
        donor.delete()
        messages.success(request, f"Donor deleted successfully. Record for {donor_name} has been removed.")
        return redirect('donor_list')

    return render(request, 'donor_confirm_delete.html', {'donor': donor})


def about_view(request):
    """About the Blood Donor Availability Management System"""
    return render(request, 'about.html')


def custom_404_view(request, exception=None):
    """Custom 404 error page"""
    return render(request, '404.html', status=404)
