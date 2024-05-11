from django.shortcuts import render, redirect
from chat.models import Resident, Item
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.sessions.models import Session
from django.utils import timezone
import csv

def home(request):
    return render(request, 'login.html')


def regency(request):
    residents = Resident.objects.all()
    items = Item.objects.all()
    return render(request, 'regency.html', {'residents': residents, 'items': items})

def add_resident(request):
    if request.method == 'POST':
        # Get data from the form
        id = request.POST.get('id')
        name = request.POST.get('name')
        # Create a new resident object
        resident = Resident.objects.create(id=id, name=name)
        # Redirect to regency page
        return redirect('regency')
    return render(request, 'add_resident.html')

def delete_resident(request, resident_id):
    if request.method == 'POST':
        try:
            # Get the resident to delete
            resident = Resident.objects.get(pk=resident_id)
            resident.delete()
            return redirect('regency')
        except Resident.DoesNotExist:
            pass  # Handle the case where resident does not exist
    return redirect('regency')  # Redirect to regency page in case of GET request

def add_item(request):
    if request.method == 'POST':
        # Get data from the form
        resident_id = request.POST.get('resident_id')
        item_name = request.POST.get('item_name')
        # Create a new item object associated with the resident
        resident = Resident.objects.get(id=resident_id)
        item = Item.objects.create(name=item_name)
        resident.items.add(item)
        # Redirect to regency page
        return redirect('regency')
    return render(request, 'add_item.html', {'residents': Resident.objects.all()})


def export_residents_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="residents.csv"'

    writer = csv.writer(response)
    writer.writerow(['Resident ID', 'Name', 'Items'])

    residents = Resident.objects.all()
    for resident in residents:
        items_list = ", ".join(item.name for item in resident.items.all())
        writer.writerow([resident.id, resident.name, items_list])

    return response


def checkview(request):
    return render(request, 'regency.html')
class RegisterView(View):
    form_class = CustomUserCreationForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, 'register.html', {'form':form})
    
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        return render(request, 'register.html', {'form': form})


from django.urls import reverse

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'login.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(reverse('regency'))  # Redirect to 'regency' URL name
        return self.form_invalid(form)
    
class CustomLogoutView(LogoutView):
    next_page = 'home'
