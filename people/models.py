from django.db import models
from django.contrib.auth.models import User
from staffing.models import Application 
from programming.models import Show, Company

class Person(models.Model):
	class Meta:
		verbose_name = 'Person'
		verbose_name_plural = 'People'

	site_user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, unique=True)
	forename = models.CharField(max_length=100)
	surname = models.CharField(max_length=100)
	middle_name = models.CharField(max_length=150, blank=True, verbose_name='Middle name(s)')
	pronouns = models.CharField(max_length=50, help_text='eg "he / him", "she / her", "they / them"', blank=True)
	photo = models.ImageField(upload_to='people_photos/', blank=True) 
	medical_info = models.TextField(blank=True)
	allergies = models.ManyToManyField('Allergy', blank=True)
	person_type = models.CharField(max_length=30,
		choices = (
			('STAFF', 'Paradise Green Staff'),
			('COMPY', 'Performing Company Member'),
			('EMGCY', 'Staff Emergency Contact')),
		default='COMPY' )

	def get_applications(self, event=None):
		if self.person_type == 'STAFF':
			qs = Application.objects.filter(person=self)
			if event: 
				return qs.filter(event_application=event)
			else:
				return qs 
		else:
			return None 

	def is_active_in_event(self, event=None):
		if not event:
			return False 
		else:
			if self.get_applications(event=event).count() > 0:
				return True 
			else:
				return False 

	def get_shows(self, event=None):
		# Get shows where this person is the lead contact, or listed in the PersonShow list 
		shows = {}
		shows['lead'] = Show.objects.filter(lead_contact=self)
		listed = PersonShow.objects.filter(person=self)
		shows['listed'] = [] 
		for s in listed:
			shows['listed'].append(s.show)
		if shows['lead'].count() == 0 and len(shows['listed']) == 0:
			return None 
		else:
			return shows

	def get_companies(self):
		lead_contacts = Company.objects.filter(lead_contact=self)
		listed_in = Company.objects.filter(company_members__in=[self.pk])
		# return lead_contacts.union(listed_in)
		return lead_contacts

	@property 
	def username(self):
		return self.site_user.username 

	def __str__(self):
		return self.forename + ' ' + self.surname 

def set_username(sender, instance, **kwargs):
    if not instance.username:
        username = (instance.first_name[:1] + instance.last_name).lower() 
        counter = 1
        while User.objects.filter(username=username):
            username = username + str(counter)
            counter += 1
        instance.username = username
models.signals.pre_save.connect(set_username, sender=User)

class PersonShow(models.Model):
	# Intermediary to be able to give people specific roles on shows 
	# This way, a company with multiple shows can have the same person in different roles on their two shows (eg producing one and the technician for another).

	class Meta:
		verbose_name = 'Person - Show Relationship'
		verbose_name_plural = 'Person - Show Relationships'

	person = models.ForeignKey(Person, on_delete=models.CASCADE, limit_choices_to={'person_type':'COMPY'})
	show = models.ForeignKey('programming.Show', on_delete=models.CASCADE)

	role = models.CharField(max_length=30,
		choices = (
			('DIR', 'Director'),
			('PRO', 'Producer'),
			('ACT', 'Performer'),
			('STG', 'Stage Manager'),
			('TCH', 'Technician'),
			('OTH', 'Other')), default='ACT')
	role_other = models.CharField(max_length=30, blank=True, verbose_name='Other:')

	def __str__(self):
		return str(self.person) + ' is ' + str(self.get_role_display()) + ' on ' + str(self.show)

class ContactDetail(models.Model):
	person = models.ForeignKey('Person', on_delete=models.CASCADE, null=True, blank=True)
	contact_reference = models.CharField(max_length=100, default='Default contact details')
	email_primary = models.EmailField(max_length=100)
	email_secondary = models.EmailField(max_length=100, blank=True)
	mobile_number = models.CharField(max_length=20, blank=True)
	phone_number = models.CharField(max_length=20, blank=True)

	post_point = models.CharField(max_length=100, blank=True)
	building_name = models.CharField(max_length=30, blank=True)
	building_number = models.CharField(max_length=10, blank=True)
	street_name = models.CharField(max_length=100, blank=True)
	city = models.CharField(max_length=100, blank=True)
	region = models.CharField(max_length=100, blank=True)
	country = models.CharField(max_length=100, blank=True)
	post_code = models.CharField(max_length=100, blank=True)

	def __str__(self):
		return self.contact_reference + ' for ' + str(self.person)

class Allergy(models.Model):
	class Meta: 
		verbose_name = 'Allergy'
		verbose_name_plural = 'Allergies'

	title = models.CharField(max_length=100)

	def __str__(self):
		return self.title 



'''

Table People.person {
  pk int 
  forename string 
  surname string 
  middle_name string 
  company string
  contact_details string [ref: > People.contacts.person]
  photo file 
  medical_info string 
}

Table People.contacts {
  person string 
  contact_reference string 
  email_1 string 
  email_2 string 
  mob_number string 
  landline_number string 
  
  post_point string 
  building_name string 
  building_number string 
  street_name string 
  city string 
  region string 
  country string 
  post_code string 
}'''