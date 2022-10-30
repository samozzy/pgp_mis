from django.urls import path 
from . import views 


app_name = 'staffing' 

urlpatterns = [ 
	
	path('event/<int:pk>/volunteer/', views.ApplicationFormView.as_view(), name='staffingCreateApplication'),
	path('applications/', views.ApplicationListView.as_view(), name='staffingApplicationList'), # current event 
	path('applications/<int:pk>/', views.ApplicationDetailView.as_view(), name='staffingApplicationDetail'),
	path('applications/<int:pk>/offer/', views.OfferFormView.as_view(), name='staffingApplicationOfferCreate'),
	path('applications/<int:pk>/review/', views.OfferUpdateView.as_view(), name='staffingApplicationOfferUpdate'),
	# path('event/<int:pk>/applications', views.ApplicationListView.as_view(), name='staffingAppliationListArchive'),

]
