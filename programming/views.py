from django.contrib import messages 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView

from programming.models import Company, Show, Slot, Offer, Invoice, Event
from people.models import Person 
from staffing.models import Application, QuickLink
from .forms import ShowForm, SlotCreationForm, CompanyForm, OfferForm

from .mixins import MISPermissionMixin, get_user_profile

# Views for the app and its models 


# def get_user_profile(user):
# 	p = Person.objects.filter(site_user = user).first()
# 	# objects.get() will raise an exception, and we want to handle the fail ourselves
# 	if p:
# 		return p 
# 	else:
# 		return False 

class HomeView(MISPermissionMixin, TemplateView):
	# basic home page offering navigation functionality to other areas of the site 
	# template_name = ''
	template_name = 'index.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data() 
		# context['user_profile'] = get_user_profile(self.request.user)
		context['applications'] = context['user_profile'].get_applications()
		if context['user_profile'].person_type == 'STAFF':
			context['available_events'] = Event.objects.filter(accepting_staff_applications=True)
			context['available_event_applications'] = context['available_events']
			for app in context['applications']:
				context['available_event_applications'] = context['available_events'].exclude(pk=app.event_application.pk)
		elif context['user_profile'].person_type == 'COMPY':
			context['available_events'] = Event.objects.filter(accepting_show_submissions=True)

		if context['user_profile'].person_type == 'STAFF':
			context['quick_links'] = QuickLink.objects.all()
		return context 

# passes test: can edit company (directors; company)
class CompanyFormView(MISPermissionMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
	permission_required = ('programming.add_company', 'programming.change_company')
	template_name = 'company_form.html'
	success_url = reverse_lazy('programming:programmingDashboard')
	form_class = CompanyForm 
	success_message = "Company details updated successfully"
	model = Company 	

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['user_profile'] = get_user_profile(self.request.user)
		return context 

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['site_user'] = self.request.user 
		return kwargs 

# passes test: can create show (directors; company)
class ShowCreateView(MISPermissionMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
	permission_required = ('programming.add_show')
	template_name = 'show_form.html'
	success_url = reverse_lazy('programming:programmingDashboard')
	form_class = ShowForm
	model = Event
	success_message = "Show created successfully"

	def get_initial(self, **kwargs):
		initial = super().get_initial()
		initial['lead_contact'] = get_user_profile(self.request.user) 
		# initial['event'] = Event.objects.get(pk=self.kwargs['pk']) # Set this to the one we've selected when starting
		return initial 

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['event'] = Event.objects.get(pk=self.kwargs['pk'])
		return context 

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['user_profile'] = get_user_profile(self.request.user)
		kwargs['site_user'] = self.request.user 
		return kwargs 

	def form_valid(self, form):
		# Manually assign the Person to the User 
		form.instance.event = Event.objects.get(pk=self.kwargs['pk'])
		return super().form_valid(form)

# passes test: can edit show (director, company)
class ShowUpdateView(MISPermissionMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
	permission_required = ('programming.change_show')
	model = Show 
	template_name = 'show_form.html'
	form_class = ShowForm 
	success_message = "Show updated successfully"

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['update'] = True 
		return context 

	def get_success_url(self, **kwargs):
		return reverse_lazy('programming:programmingShowDetail', kwargs={'pk': self.object.pk }) 

class ShowListView(MISPermissionMixin, generic.ListView):
	model = Show 
	template_name = 'show_list.html'
	context_object_name = 'shows'

	def get_event(self, **kwargs):
		if self.kwargs:
			print(self.kwargs)
			return Event.objects.get(pk=self.kwargs['pk'])
		else:
			return Event.objects.last() 

	def get_queryset(self, **kwargs):
		if get_user_profile(self.request.user).person_type == 'COMPY':
			qs = get_user_profile(self.request.user).get_shows()['lead']
			if self.kwargs and self.kwargs['pk']:
				return qs.filter(event=self.kwargs['pk'])
			else:
				return qs
		return Show.objects.filter(event=self.get_event().pk)

	def get_context_data(self, **kwargs):
		context = super(ShowListView, self).get_context_data()
		context['event'] = self.get_event() 
		return context 

class ShowListPendingView(PermissionRequiredMixin, ShowListView):
	permission_required = ('programming.dir_can_make_offer', 'programming.dir_can_administrate_shows')
	permission_denied_message = "This is a directors-only area, sorry!"

	def get_queryset(self, **kwargs):
		qs = super(ShowListView, self).get_queryset()
		return qs.filter(offer=None).filter(slot__isnull=False)

	def get_context_data(self, **kwargs):
		context = super(ShowListPendingView, self).get_context_data()
		context['page_heading'] = "Shows currently without an offer"
		return context 

class ShowDetailView(MISPermissionMixin, generic.DetailView):
	model = Show 
	template_name = 'show_detail.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		if context['user_profile'].person_type == 'COMPY':
			context['can_edit'] = True 
		return context 

# can create slot: company; director 
class SlotCreateView(MISPermissionMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
	permission_required = ('programming.add_slot')
	model = Show 
	template_name = 'slot_form.html'
	form_class = SlotCreationForm 
	success_message = "Slot application added successfully"

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['show'] = Show.objects.get(pk=self.kwargs['pk'])
		return context 

	def get_form_kwargs(self):
		# Pass the Show to the form to only list Weeks for Show.Event 
		kwargs = super().get_form_kwargs()
		kwargs['show'] = Show.objects.get(pk=self.kwargs['pk'])
		return kwargs

	def get_initial(self):
		initial = super().get_initial()
		this_show = Show.objects.get(pk=self.kwargs['pk'])
		if this_show.get_slots():
			highest_pref = max(this_show.get_slot_preferences())
			initial['slot_preference'] = highest_pref + 1
		else:
			initial['slot_preference'] = 1 
		return initial 

	def form_valid(self, form):
		# Manually assign the Show to the Slot 
		form.instance.show = Show.objects.get(pk=self.kwargs['pk'])
		return super().form_valid(form)

	def get_success_url(self):
		# Go back to the show 
		return reverse_lazy('programming:programmingShowDetail', kwargs={'pk': self.object.show.pk })

class SlotListView(MISPermissionMixin, PermissionRequiredMixin, generic.ListView):
	permission_required = ('programming.add_slot', 'programming.dir_can_make_offer')
	model = Slot 
	template_name = 'slot_list.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['show'] = Show.objects.get(pk=self.kwargs['pk'])
		return context 

class OfferCreateView(MISPermissionMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = ('programming.change_slot', 'programming.dir_can_make_offer')
	permission_denied_message = "Only directors can make offers to shows."
	model = Offer 
	template_name = 'offer_form.html'
	form_class = OfferForm 

	def dispatch(self, *args, **kwargs):
		if Offer.objects.filter(show=Show.objects.get(pk=self.kwargs['pk'])):
			messages.add_message(self.request, messages.ERROR, "This show already has an offer attached")
			return redirect(reverse_lazy('programming:programmingShowDetail', kwargs={'pk': self.kwargs['pk'] }))
		else: 
			return super(OfferCreateView, self).dispatch(*args, **kwargs)

	def get_success_url(self, **kwargs):
		return reverse_lazy('programming:programmingShowDetail', kwargs={'pk': self.kwargs['pk'] })

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['show'] = Show.objects.get(pk=self.kwargs['pk'])
		context['slot'] = Slot.objects.get(pk=self.kwargs['slot_pk'])
		context['create'] = True 
		return context 

	def form_valid(self, form):
		# Give it all the info and force a pending offer for the right show and slot to be created
		# Maaaagic 
		form.instance.show = Show.objects.get(pk=self.kwargs['pk'])
		form.instance.slot = Slot.objects.get(pk=self.kwargs['slot_pk'])
		form.instance.status = 'PEN'
		return super().form_valid(form)

class OfferUpdateView(MISPermissionMixin, PermissionRequiredMixin, generic.UpdateView):
	permission_required = ('programming.change_offer') 
	template_name = 'offer_form.html'
	form_class = OfferForm 
	model = Offer 

	def get_object(self, **kwargs):
		try:
			return Offer.objects.get(show=Show.objects.get(pk=self.kwargs['pk']))
		except:
			messages.add_message(self.request, messages.ERROR, "There is no offer currently attached to this show.")
			raise Http404

	def get_success_url(self, **kwargs):
		return reverse_lazy('programming:programmingShowDetail', kwargs={'pk': self.kwargs['pk'] })

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['show'] = Show.objects.get(pk=self.kwargs['pk'])
		context['offer'] = context['show'].offer 
		return context 

# user-passes-test = is_authenticated 
class CompanyListView(MISPermissionMixin, generic.ListView):
	model = Company 
	template_name = 'company-list.html'

	# 1. Is staff member - show all 
	# 2. Is company member - show only their companies 

class CompanyDetailView(MISPermissionMixin, generic.DetailView):
	model = Company 
	template_name = 'company-detail.html'

	# 1. Is staff member - show 
	# 2. Is company where user.get_companies() contains company 

class CompanyInvoiceView(MISPermissionMixin, generic.ListView):
	model = Invoice 
	template_name = 'invoice-company.html'

	# get context data = invoices.company

	# 1. is member of this company 
	# 2. is director 

# user-passes-test = is_director 
class InvoiceListView(generic.ListView):
	model = Invoice 
	template_name = 'invoice-list.html'

class InvoiceDetailView(generic.ListView):
	model = Invoice 
	template_name = 'invoice-list.html'

# user-passes-test = is_volunteer 
class EventListView(MISPermissionMixin, generic.ListView):
	model = Event 
	template_name = 'event_list.html'
	context_object_name = 'event_list'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data()
		context['user_profile'] = get_user_profile(self.request.user)
		return context 

	# def get_queryset(self, *args, **kwargs):
	# 	qs = Show.objects.filter(event=self.kwargs['pk'])
	# 	if get_user_profile(self.request.user).person_type == 'COMPY':
	# 		qs.filter(lead_contact=get_user_profile(self.request.user))
	# 	return qs

# user-passes-test = is_volunteer 
class EventOffersView(generic.ListView):
	model = Show 
	template_name = 'event-shows-offers.html'

	# get_context_data = Show.event = event.pk 
	# show.filter(has_offer() )

# user-passes-test = is_volunteer 
class EventAllView(generic.ListView):
	model = Show 
	template_name = 'event-shows-all.html'

	# get_context_data = Show.event = event.pk | no filter 