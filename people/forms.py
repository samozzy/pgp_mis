from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Person 

class UserRegistrationForm(UserCreationForm):
	email = forms.EmailField(required=True)
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)

	class Meta:
		model = User
		fields = ("first_name", "last_name", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(UserRegistrationForm, self).save(commit=False)
		user.email = self.cleaned_data['email']

		# TODO: Create a UserProfile based on whether this is a company or volunteer registration 
		if commit:
			user.save()
		return user

class PersonCreationForm(forms.ModelForm):
	class Meta:
		model = Person 
		fields = ("forename", "middle_name", "surname", "pronouns", "person_type")
		widgets = {
			'person_type': forms.RadioSelect(),
		}

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['person_type'].widget.attrs.update({'class': 'form-check-input'})

class PersonUpdateForm(forms.ModelForm):
	class Meta:
		model = Person 
		fields = ("forename", "middle_name", "surname", "pronouns")