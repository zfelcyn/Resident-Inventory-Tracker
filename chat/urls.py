from django.urls import path
from . import views

urlpatterns = [
    # Other paths...
    path('login/', views.CustomLoginView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('chat/logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('add_resident/', views.add_resident, name='add_resident'),
    path('add_item/', views.add_item, name='add_item'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('add_comment/', views.add_comment, name='add_comment'),
    path('delete_resident/<int:resident_id>/', views.delete_resident, name='delete_resident'),
    path('export_residents_csv/', views.export_residents_csv, name='export_residents_csv'),
    path('regency/', views.regency, name='regency'),
    path('resident/<int:resident_id>/', views.resident_detail, name='resident_detail'),  # New path for resident details
]
  