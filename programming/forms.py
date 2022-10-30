from django import forms 

from .models import Show, Event, Company, Slot, Week, Offer
from people.models import Person 

class ShowForm(forms.ModelForm):
	class Meta:
		model = Show 
		fields = ("show_title", "company", "lead_contact", "level",
			"outline", "motivation", "funding",
			"copy_short", "copy_long",
			"set_outline", "tech_outline",
			"cast_size", "crew_size",
			"show_duration", "get_in_dur", "get_out_dur")
		# Company choices limited to companies for which self.user is a member 
		# lead_contacts is limited to self.user AND any company members of the selected company

	def __init__(self, *args, **kwargs):
		# Get the user_profile kwarg from get_form_kwargs in the view, and use it to filter to the user's companies 
		self.user_profile = kwargs.pop('user_profile', None)
		self.site_user = kwargs.pop('site_user', None)
		super(ShowForm, self).__init__(*args, **kwargs)
		self.fields['company'].queryset = Person.objects.filter(site_user=self.site_user).first().get_companies()
		self.fields['lead_contact'].queryset = Person.objects.filter(site_user=self.site_user)

class SlotCreationForm(forms.ModelForm):
	class Meta:
		model = Slot 
		fields = ("venue", "show_start_time", "show_end_time", "slot_preference", "week")

		widgets = {
			'week': forms.CheckboxSelectMultiple(),
		}

	def __init__(self, *args, **kwargs):
		self.show = kwargs.pop('show', None)
		super(SlotCreationForm, self).__init__(*args, **kwargs)
		self.fields['week'].queryset = Week.objects.filter(event=self.show.event).filter(has_performances=True)

class CompanyForm(forms.ModelForm):
	class Meta: 
		model = Company 
		fields = ("company_name", "company_email", "company_website", "lead_contact")

	def __init__(self, *args, **kwargs):
		self.site_user = kwargs.pop('site_user', None)
		super(CompanyForm, self).__init__(*args, **kwargs)
		self.fields['lead_contact'].queryset = Person.objects.filter(site_user=self.site_user)

class OfferForm(forms.ModelForm):
	class Meta:
		model = Offer 
		fields = ("status",)