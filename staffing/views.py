from django.contrib import messages 
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView

from programming.models import Event 
from staffing.models import Application, QuickLink, Offer
from .forms import ApplicationForm, OfferForm 

from programming.mixins import MISPermissionMixin, get_user_profile

# Views for the app and its models 

class ApplicationFormView(PermissionRequiredMixin, MISPermissionMixin, SuccessMessageMixin, CreateView):
# passes test: can edit company (directors; company)
	permission_required = ('staffing.add_application')
	template_name = 'application_form.html'
	success_url = reverse_lazy('programming:programmingDashboard')
	form_class = ApplicationForm 
	success_message = "Application submitted successfully"
	model = Application 	

	def get_object(self, **kwargs):
		return Event.objects.get(pk=self.kwargs['pk'])

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['event'] = Event.objects.get(pk=self.kwargs['pk'])
		return context 

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['event'] = self.kwargs['pk']
		return kwargs 

	def form_valid(self, form):
		# Manually assign the Application to the Person  
		form.instance.person = get_user_profile(self.request.user)
		form.instance.event_application = Event.objects.get(pk=self.kwargs['pk'])
		return super().form_valid(form)

class ApplicationListView(PermissionRequiredMixin, MISPermissionMixin, generic.ListView):
	permission_required = ('staffing.change_application', 'staffing.dir_can_offer_application')
	permission_denied_message = "Only directors can view applications"
	model = Application 
	template_name = 'application_list.html'
	context_object_name = 'applications'

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		if self.kwargs and self.kwargs['pk']:
			context['event'] = Event.objects.get(pk=self.kwargs['pk'])
		else:
			context['event'] = Event.objects.last() 
		return context 

class ApplicationDetailView(MISPermissionMixin, PermissionRequiredMixin, generic.DetailView):
	permission_required = ('staffing.view_application')
	model = Application 
	template_name = "application_detail.html"

class OfferFormView(MISPermissionMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = ('staffing.add_offer',)
	template_name = 'application_offer_form.html'
	model = Application 
	form_class = OfferForm
	success_url = reverse_lazy('staffing.staffingApplicationList')

	def dispatch(self, *args, **kwargs):
		if Offer.objects.filter(application=Application.objects.get(pk=self.kwargs['pk'])):
			messages.add_message(self.request, messages.ERROR, "This application already has an offer attached")
			return redirect(reverse_lazy('staffing:staffingApplicationDetail', kwargs={'pk': self.kwargs['pk'] }))
		else: 
			return super(OfferFormCreateView, self).dispatch(*args, **kwargs)

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['event'] = Application.objects.get(pk=self.kwargs['pk']).event_application
		return kwargs 

	def form_valid(self, form):
		# Manually assign the Application to the Person  
		form.instance.application = Application.objects.get(pk=self.kwargs['pk'])
		form.instance.status = 'PEN'
		return super().form_valid(form)

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['create'] = True 
		context['application'] = Application.objects.get(pk=self.kwargs['pk'])
		return context 

class OfferUpdateView(MISPermissionMixin, PermissionRequiredMixin, generic.UpdateView):
	permission_required = ('staffing.change_offer')
	template_name = 'application_offer_form.html' 
	model = Offer 
	form_class = OfferForm 
	success_url = reverse_lazy('programming:programmingDashboard')

	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs['event'] = Application.objects.get(pk=self.kwargs['pk']).event_application
		return kwargs 

	def get_object(self, **kwargs):
		try:
			return Offer.objects.get(application=Application.objects.get(pk=self.kwargs['pk']))
		except:
			messages.add_message(self.request, messages.ERROR, "There is no offer currently attached to this application.")
			raise Http404

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['application'] = Application.objects.get(pk=self.kwargs['pk'])
		context['offer'] = context['application'].offer 
		return context 

	def form_valid(self, form):
		form.instance.weeks.set = Offer.objects.get(application=Application.objects.get(pk=self.kwargs['pk'])).weeks
		return super().form_valid(form)