from django.urls import path 
from . import views 

app_name = 'programming' 

urlpatterns = [ 

	path('', views.HomeView.as_view(), name='programmingDashboard'),
	path('shows/', views.ShowListView.as_view(), name='programmingShowList'), # Uses the "current" Event 
	path('shows/pending/', views.ShowListPendingView.as_view(), name='programmingShowPending'),
	path('shows/<int:pk>/', views.ShowDetailView.as_view(), name='programmingShowDetail'),
	path('shows/<int:pk>/edit/', views.ShowUpdateView.as_view(), name='programmingShowUpdate'),

	path('shows/<int:pk>/newslot/', views.SlotCreateView.as_view(), name='programmingSlotCreation'),
	path('shows/<int:pk>/slots/', views.SlotListView.as_view(), name='programmingSlotList'),

	path('shows/<int:pk>/<int:slot_pk>/offer/', views.OfferCreateView.as_view(), name='programmingSlotOffer'),
	path('shows/<int:pk>/offer/', views.OfferUpdateView.as_view(), name='programmingOfferUpdate'),
	# path('shows/<int:pk>/offer/confirm/', views.SlotOfferConfirm.as_view(), name='programmingSlotOfferConfirm'),
	
	path('companies/', views.CompanyListView.as_view(), name='programmingCompanyList'),
	path('companies/<int:pk>/', views.CompanyDetailView.as_view(), name='programmingCompanyDetail'),
	path('companies/<int:pk>/edit/', views.CompanyFormView.as_view(), name='programmingCompanyForm'),
	path('companies/<int:pk>/invoices/', views.CompanyInvoiceView.as_view(), name='programmingCompanyInvoice'),
	
	path('invoices/', views.InvoiceListView.as_view(), name='programmingInvoiceList'),
	path('invoices/<int:pk>/', views.InvoiceDetailView.as_view(), name='programmingInvoiceDetail'),
	
	path('event/', views.EventListView.as_view(), name='programmingEventList'), # Lists all events for archive use 
	path('event/<int:pk>/', views.ShowListView.as_view(), name='programmingEventDetail'), # Same as programmingShowList but specific Event
	path('event/<int:pk>/all/', views.EventAllView.as_view(), name='programmingEventAll'),
	
	path('event/<int:pk>/perform/', views.ShowCreateView.as_view(), name='programmingCreateShow'),
	# shows/ 
	# show/<int:pk>
		# with functionality to view their slot preferences and make them an offer 
		# with functionality to view a list of invoices associated with the show 
		# with functionality to do comments / voting 
	# companies/
	# companies/<int:pk>/
	# companies/<int:pk/invoices/ - invoices for a given company 
	# invoices/ 
	# invoices/<int:pk>/ - specific invoices 
	# event/ - event list 
	# event/<int:pk>/ - shows that have been offered a slot 
	# event/<int:pk>/all/ - all shows registered with the event
]