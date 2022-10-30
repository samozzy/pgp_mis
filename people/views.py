from django.contrib.auth.models import Group
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView, FormView

from .models import Person
from people.forms import PersonCreationForm, PersonUpdateForm
from programming.mixins import MISPermissionMixin, get_user_profile, put_user_in_group 

# Create your views here.

# passes test: is their own person or director
class PersonDetailView(MISPermissionMixin, TemplateView):
	model = Person 
	template_name = 'person_details.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data() 
		context['page_heading'] = "Your personal details"
		return context 

# passes test: can add people 
# if get_user_profile, don't attach the user to the Profile (might be a contact or other company member)
class PersonCreateView(CreateView, MISPermissionMixin, SuccessMessageMixin):
	template_name = 'person_details.html'
	success_url = reverse_lazy('programming:programmingDashboard')
	form_class = PersonCreationForm
	success_message = "You've registered successfully."
	model = Person 

	def dispatch(self, *args, **kwargs):
		# If we have a logged in user with a user profile, redirect to the edit screen 
		if get_user_profile(self.request.user):
			return redirect(reverse_lazy('people:personUpdate'))
		else:
			return super(PersonCreateView, self).dispatch(*args, **kwargs)

	def get_initial(self, **kwargs):
		# When we don't have a Person object, we prefill from the User object
		initial = super().get_initial() 
		initial['forename'] = self.request.user.first_name 
		initial['surname'] = self.request.user.last_name 
		return initial 

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['use_form'] = True 
		return context 

	def form_valid(self, form):
		# Manually assign the Person to the User 
		form.instance.site_user = self.request.user 
		if form.cleaned_data['person_type'] == 'STAFF':
			put_user_in_group(self.request.user, 'volunteer')
		elif form.cleaned_data['person_type'] == 'COMPY':
			put_user_in_group(self.request.user, 'company')
		# Put the user in a permission group so that we can work with them 
		return super().form_valid(form)

# can edit people 
class PersonUpdateView(MISPermissionMixin, SuccessMessageMixin, UpdateView):
	model = Person 
	template_name = 'person_details.html'
	success_url = reverse_lazy('people:personDetail')
	form_class = PersonUpdateForm
	success_message = "Update successful." 

	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['use_form'] = True 
		if get_user_profile(self.request.user):
			context['page_heading'] = "Update Personal Information"
			context['user_profile'] = get_user_profile(self.request.user)
		return context 

	def get_object(self, **kwargs):
		return get_user_profile(self.request.user)

	# def get_initial(self, **kwargs):
	# 	# A
	# 	initial = super().get_initial() 
	# 	if get_user_profile(self.request.user):
	# 		profile = get_user_profile(self.request.user)
	# 		initial['forename'] = profile.forename 
	# 		initial['surname'] = profile.surname 
	# 		initial['middle_name'] = profile.middle_name 
	# 		initial['pronouns'] = profile.pronouns 
	# 	return initial 


