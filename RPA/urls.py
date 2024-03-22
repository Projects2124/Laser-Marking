from django.urls import path
from . import views

urlpatterns=[
    path('', views.user_login, name='login'),
    path('partname/', views.Part, name='partname'),

    path('Part/', views.Part, name='Part'),
    path('Part_edit/<int:pk>/', views.Part_edit, name='Part_edit'),
    path('Part_delete/<int:pk>/',views.Part_delete, name='Part_delete'),

    path('data_screen/',views.data_screen, name='data_screen'),
    # path('fetch_data/',views.fetch_data, name='fetch_data'),
    
    
    path('logout/', views.logout_view, name='logout'),

]