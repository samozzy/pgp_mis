from django.db import models

# Create your models here.

class StaffRole(models.Model):
	class Meta: 
		ordering = ['department','role_name']
	role_name = models.CharField(max_length=100, blank=True, unique=True, help_text="A role offered on the staff, eg. Technician")
	department = models.CharField(max_length=50, 
		choices = (
			('H', 'Front of House'),
			('K', 'Kitchen'),
			('T', 'Technical'),
			('A', 'Administration'),
			('D', 'Duty')
		),
		default='H')
	is_management = models.BooleanField(default=False)
	appears_in_application = models.BooleanField(default=True, help_text="Deselect for special roles only appearing on the rota and not selectable in the volunteer application form, eg. 'Other', 'Build Manager', etc.")

	def __str__(self):
		return self.role_name

class Application(models.Model):
	class Meta:
		permissions = [
			('dir_can_offer_application', 'Can review and offer applications')
		]
		verbose_name = 'Volunteer Application'
		verbose_name_plural = 'Volunteer Applications'
		unique_together = ['person','event_application']
		# A person may only have one application for a particular event
		# TODO: Unique together: roles_willing, roles_desired, roles_declined
		# Not currently implemented because nice error handling would be a fine thing 

	person = models.ForeignKey('people.Person', on_delete=models.CASCADE, null=True)
	# This is a ForeignKey because a person can have applications with multiple events
	roles_willing = models.ManyToManyField(StaffRole, related_name='roles_willing', blank=True)
	roles_desired = models.ManyToManyField(StaffRole, related_name='roles_desired', blank=True)
	roles_declined = models.ManyToManyField(StaffRole, related_name='roles_declined', blank=True)

	person_bio = models.TextField()
	event_application = models.OneToOneField('programming.Event', on_delete=models.SET_NULL, null=True)
	weeks_available = models.ManyToManyField('programming.Week')
	status = models.CharField(max_length=30,
		choices = (
			('ACC', 'Offer accepted'),
			('OFF', 'Offer made'),
			('REJ', 'Offer rejected'),
			('APP', 'Application complete'),
			('INC', 'Application started'),
			('WIT', 'Application withdrawn')
		),
		default='INC',
		verbose_name='Application status',
	)

	@property 
	def long_name(self):
		return self + ' for ' + str(self.person)

	@property 
	def has_management_roles(self):
		for role in self.roles_desired.all():
			if role.is_management:
				return True 
		for role in self.roles_willing.all():
			if role.is_management:
				return True 
		return False 

	def __str__(self):
		return str(self.person) + ' application for ' + str(self.event_application) 

class WeekPreference(models.Model):
	class Meta:
		ordering = ['order']

	application = models.ForeignKey(Application, on_delete=models.CASCADE, null=True)
	weeks = models.ManyToManyField('programming.Week')
	order = models.IntegerField(unique=True)

class Offer(models.Model):
	class Meta:
		verbose_name = 'Volunteer Offer'
		verbose_name_plural = 'Volunteer Offers'

	application = models.OneToOneField(Application, on_delete=models.CASCADE)
	weeks = models.ManyToManyField('programming.Week')
	status = models.CharField(max_length=10,
		choices = (
			('PEN', 'Pending'),
			('ACC', 'Accepted'),
			('REJ', 'Rejected'),
		),
		default = 'PEN'
	)	

	def __str__(self):
		return 'Offer for ' + str(self.application.person) + ' (' + str(self.get_status_display()) + ', ' + str(self.application.event_application) + ')'

class QuickLink(models.Model):
	class Meta:
		ordering = ['ordering']
		verbose_name = 'Quick Link'
		verbose_name_plural = 'Quick Links'

	title = models.CharField(max_length=100,blank=True, help_text='How the link appears, eg "Rota"')
	link = models.URLField(blank=True, help_text="The full link to the page, don't forget the https://!")
	ordering = models.IntegerField(default=1)

	def __str__(self):
		return 'Quick link for ' + self.title