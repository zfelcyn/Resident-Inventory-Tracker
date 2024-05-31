from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('regency/', views.regency, name='regency'),
    path('resident/<int:resident_id>/', views.resident_detail, name='resident_detail'),
    path('add_resident/', views.add_resident, name='add_resident'),
    path('delete_resident/<int:resident_id>/', views.delete_resident, name='delete_resident'),
    path('add_items/', views.add_items, name='add_items'),  # Add this line
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('export_residents_csv/', views.export_residents_csv, name='export_residents_csv'),
    path('checkview/', views.checkview, name='checkview'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('chat/logout/', views.CustomLogoutView.as_view(), name='logout'),
]