from django.shortcuts import render, redirect
from chat.models import Resident, Item, Comment
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView, LogoutView
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.sessions.models import Session
from django.utils import timezone
from .utils import generate_resident_word
from django.db import transaction
from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
import csv

def home(request):
    return render(request, 'login.html')

def regency(request):
    letter = request.GET.get('letter')
    search_query = request.GET.get('search')

    if search_query:
        residents = Resident.objects.filter(first_name__icontains=search_query) | Resident.objects.filter(last_name__icontains=search_query)
    elif letter:
        residents = Resident.objects.filter(last_name__istartswith=letter)
    else:
        residents = Resident.objects.none()  # Return an empty queryset if no filter is applied

    return render(request, 'regency.html', {'residents': residents})


def resident_detail(request, resident_id):
    resident = get_object_or_404(Resident, pk=resident_id)
    items = resident.items.all()
    comments = resident.comments.all()

    if 'generate_word' in request.GET:
        return generate_resident_word(resident)

    return render(request, 'resident_detail.html', {
        'resident': resident,
        'items': items,
        'comments': comments
    })


def add_resident(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_admittance = request.POST.get('date_of_admittance')
        # Create a new resident object
        resident = Resident.objects.create(id=id, first_name=first_name, last_name=last_name, date_of_admittance=date_of_admittance)
        # Redirect to regency page
        return redirect('regency')
    return render(request, 'add_resident.html')

# Delete resident 

def delete_resident(request, resident_id):
    # Get the resident object to delete
    resident = get_object_or_404(Resident, id=resident_id)
    
    if request.method == 'POST':
        # Delete the resident object
        resident.delete()
        # Redirect to regency page
        return redirect('regency')
    
    return render(request, 'delete_resident.html', {'resident': resident})


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


def delete_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    resident = item.resident_set.first()

    if request.method == 'POST':
        reason = request.POST.get('reason')
        if reason == 'resident':
            comment_text = f"{item.name} removed by resident"
        else:
            comment_text = f"{item.name} removed by family member"
        Comment.objects.create(resident=resident, content=comment_text)
        item.delete()
        return redirect('regency')

    return render(request, 'confirm_delete.html', {'item': item, 'resident': resident})

def add_comment(request):
    if request.method == 'POST':
        # Get data from the form
        resident_id = request.POST.get('resident_id')
        comment_content = request.POST.get('comment_content')
        
        # Create a new comment object associated with the resident
        resident = Resident.objects.get(id=resident_id)
        comment = Comment.objects.create(resident=resident, content=comment_content)
        
        # Redirect to regency page
        return redirect('regency')
    
    return render(request, 'regency.html', {'residents': Resident.objects.all()})

def export_residents_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="residents.csv"'

    writer = csv.writer(response)
    writer.writerow(['Resident ID', 'Name', 'Items', 'Comments'])

    residents = Resident.objects.all()
    for resident in residents:
        items_list = ", ".join(item.name for item in resident.items.all())
        comments_list = "; ".join(comment.content for comment in resident.comments.all())
        writer.writerow([resident.id, resident.name, items_list, comments_list])

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
