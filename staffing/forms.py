from django import forms 
from django.utils.text import slugify 

from .models import Application, StaffRole, Offer
from people.models import Person 
from programming.models import Event, Week

class ApplicationForm(forms.ModelForm):
	# Staffing application form (company / show applications are in the programming app)
	class Meta:
		model = Application 
		fields = ("roles_willing", "roles_desired", "roles_declined",
			"person_bio", "weeks_available")
		widgets = {
			'roles_willing': forms.CheckboxSelectMultiple(),
			'roles_desired': forms.CheckboxSelectMultiple(),
			'roles_declined': forms.CheckboxSelectMultiple(),
			'weeks_available': forms.CheckboxSelectMultiple(), 
		}

	def __init__(self, *args, **kwargs):
		# Get the user_profile kwarg from get_form_kwargs in the view, and use it to filter to the user's companies 
		self.event = kwargs.pop('event', None)
		super(ApplicationForm, self).__init__(*args, **kwargs)
		self.fields['weeks_available'].queryset = Week.objects.filter(event=self.event)
		self.fields['roles_willing'].queryset = StaffRole.objects.filter(appears_in_application=True)
		self.fields['roles_desired'].queryset = StaffRole.objects.filter(appears_in_application=True)
		self.fields['roles_declined'].queryset = StaffRole.objects.filter(appears_in_application=True)

		'''
		## Manually add a bunch of custom fields for the available roles
		# for role in StaffRole.objects.filter(appears_in_application=True):
		# 	self.fields[slugify(str(role.role_name))] = forms.ChoiceField(
		# 		label=str(role.role_name),
		# 		choices = (
		# 			('1', 'I would not like to do this role'),
		# 			('2', 'I can do this role if required'),
		# 			('3', 'I would like to do this role')
		# 		),
		# 	)
		'''

class OfferForm(forms.ModelForm):
	class Meta:
		model = Offer 
		fields = ('weeks', 'status')
		widgets = {
			'weeks': forms.CheckboxSelectMultiple(),
		}

	def __init__(self, *args, **kwargs):
		self.event = kwargs.pop('event', None)
		super(OfferForm, self).__init__(*args, **kwargs)
		self.fields['weeks'].queryset = Week.objects.filter(event=self.event)
