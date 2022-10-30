from django.urls import path 
from . import views 

app_name = 'people' 

urlpatterns = [ 
	path('person/', views.PersonDetailView.as_view(), name='personDetail'),
	path('person/setup/', views.PersonCreateView.as_view(), name='personSetUp'),
	path('person/edit/', views.PersonUpdateView.as_view(), name='personUpdate'),
]