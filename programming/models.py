import datetime 
from django.db import models

# Create your models here.

class Week(models.Model):
	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['title', 'event'], name='unique_weeks_in_event')
		]

	title = models.CharField(max_length=50,
		choices = (
			('W0', 'Week 0 Start'),
			('W1', 'Week 1 Start'),
			('W2', 'Week 2 Start'),
			('W3', 'Week 3 Start'),
			('W4', 'Week 4 Start'),
		),
	)
	date = models.DateField()
	event = models.ForeignKey('Event', on_delete=models.CASCADE)
	offers_preview = models.BooleanField(default=False)
	has_performances = models.BooleanField(default=True, help_text="Whether there are performances on this week. Eg W0 and W4 will likely not.")

	def __str__(self):
		return self.title + ' for ' + str(self.event) + ' (starts ' + str(self.date) + ')'

class Event(models.Model):
	class Meta:
		ordering = ['year']

	title = models.CharField(max_length=250, default='Edinburgh Fringe', help_text='What is the event? (Typically you won\'t change this)')
	year = models.IntegerField(unique=True, null=True, help_text='The year the event is taking place. The latest year will be used as the default year for "current" lists.')
	accepting_show_submissions = models.BooleanField(default=True, help_text="Accepting submissions for show registration")
	accepting_staff_applications = models.BooleanField(default=False, help_text="Accepting applications for staff")

	def __str__(self):
		if self.year:
			return self.title + ' ' + str(self.year)
		else:
			return self.title

class Company(models.Model):
	class Meta: 
		verbose_name = 'Performing Company'
		verbose_name_plural = 'Performing Companies'

	company_name = models.CharField(
		max_length=50
	)
	company_email = models.CharField(
		max_length=150
	)
	company_website = models.CharField(
		max_length=200,
		blank=True
	)
	lead_contact = models.ForeignKey('people.Person', on_delete=models.SET_NULL, null=True, related_name='lead_contact', limit_choices_to={'person_type':'COMPY'})
	company_members = models.ManyToManyField('people.Person', related_name='company_members', blank=True, limit_choices_to={'person_type':'COMPY'})

	def get_shows(self):
		return Show.objects.filter(company=self)

	def save(self, *args, **kwargs):
		# Ensure that the lead contact is a company member. Rather than invalidating the form, we'll just add them if they've not been selected 
		# Note: This won't work in the admin :eyeroll: 
		super(Company, self).save(*args, **kwargs)
		self.company_members.add(self.lead_contact)

	def __str__(self):
		return self.company_name

class Venue(models.Model):
	class Meta:
		ordering = ['title']

	title = models.CharField(max_length = 20, help_text="The short name, eg A1", unique=True)
	full_name = models.CharField(max_length=100, help_text="The long name, eg The Sanctuary")
	parent_venue = models.CharField(
		max_length=30,
		choices = (
			('AUG', 'Paradise in Augustines'),
			('VAU', 'Paradise in The Vault'),),
		default='AUG'
	)

	def __str__(self):
		return self.full_name + ' (' + self.title + ')'


class Offer(models.Model):
	class Meta:
		permissions = [ 
			('dir_can_make_offer', 'Can make offer')
		]
	show = models.OneToOneField('Show', on_delete=models.CASCADE, null=True)
	slot = models.OneToOneField('Slot', on_delete=models.CASCADE, null=True)
	status = models.CharField(max_length=10,
		choices = (
			('PEN', 'Pending'),
			('ACC', 'Accepted'),
			('REJ', 'Rejected'),
		),
		default = 'PEN'
	)	

	def __str__(self):
		return str(self.get_status_display()) + ' offer for ' + str(self.show)

class Show(models.Model):
	class Meta:
		permissions = [ 
			('dir_can_administrate_shows', 'Can be administrator of a show')
		]

	show_title = models.CharField(max_length=200)
	company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, blank=True)
	lead_contact = models.ForeignKey('people.Person', on_delete=models.SET_NULL, null=True, related_name='show_lead_contact')
	# The lead contact for the show and the company might be different 
	status = models.CharField(
		max_length=30,
		choices = (
			('DRA', 'Draft'),
			('APP', 'Application Submitted (waiting for an offer)'),
			('COM', 'Complete'),
		),
		default = 'DRA',
		help_text = 'Application status',
	)
	level = models.CharField(
		max_length=30,
		choices = (
			('PRO', 'Professional'),
			('EME', 'Emerging Professional'),
			('SEM', 'Semi-Professional'),
			('AMA', 'Amateur'),
		),
		default = 'PRO',
		help_text = 'How established is the company?'
	)
	outline = models.TextField(blank=True) 
	motivation = models.TextField(blank=True)
	funding = models.TextField(blank=True)
	copy_short = models.TextField(blank=True, help_text="Around 50 words", verbose_name="Marketing copy (short)")
	copy_long = models.TextField(blank=True, help_text="Around 100 words", verbose_name="Marketing copy (long)")
	set_outline = models.TextField(blank=True)
	tech_outline = models.TextField(blank=True)
	cast_size = models.IntegerField(default=0)
	crew_size = models.IntegerField(default=0)
	show_duration = models.DurationField(default=0) 
	get_in_dur = models.DurationField(default=0, verbose_name="Get-in duration") 
	get_out_dur = models.DurationField(default=0, verbose_name="Get-out duration")
	event = models.ForeignKey(Event, on_delete=models.PROTECT)
	notes_general = models.TextField(blank=True, verbose_name="Notes (general)")
	via_link = models.CharField(max_length=200, blank=True, verbose_name='VIA Box Office Link')
	poster = models.ImageField(blank=True, null=True)

	def get_people(self):
		defined_people = PersonShow.objects.filter(show=self)
		return defined_people.union(self.lead_contact)

	def get_slots(self):
		return Slot.objects.filter(show=self) or None 

	def get_slot_preferences(self):
		if self.get_slots():
			prefs = [] 
			for s in self.get_slots():
				prefs.append(s.slot_preference)
			return prefs 
		else:
			return 0 

	def get_comments(self):
		return Comment.objects.filter(show=self) or None 

	def get_votes(self):
		return Vote.objects.filter(show=self) or None 

	def __str__(self):
		return_string = self.show_title
		if self.company:
			return_string += ' from ' + str(self.company)
		return return_string

class Slot(models.Model):
	class Meta:
		ordering = ['show', 'slot_preference']
		constraints = [
			models.UniqueConstraint(fields=['show', 'slot_preference'], name='unique_slot_preference')
		]

	show = models.ForeignKey(Show, on_delete=models.CASCADE, null=True)
	venue = models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True)
	show_start_time = models.TimeField(help_text='SHOW, not slot, start time', null=True)
	show_end_time = models.TimeField(help_text='SHOW, not slot, end time', null=True)
	slot_price = models.DecimalField(max_digits=8, decimal_places=2,null=True,blank=True)
	slot_guarantee = models.DecimalField(max_digits=8, decimal_places=2,null=True,blank=True)
	box_office = models.DecimalField(max_digits=8, decimal_places=2,null=True,blank=True)
	slot_preference = models.PositiveSmallIntegerField(default=1)
	has_preview = models.BooleanField(default=False, verbose_name='Add a preview performance')
	slot_status = models.CharField(max_length=20,
		choices = (
			('REQ', 'Requested'),
			('OFF', 'Offered'),
			('ACC', 'Accepted'),
			('REJ', 'Rejected')),
		default='REQ')

	week = models.ManyToManyField(Week)
	# Add validator that only shows in available weeks can have a preview 

	def show_duration(self):
		return self.show.duration 
	# Need to make a datetime object, give it the times, and then do the math
	def slot_timings(self):
		start_date = self.week.first().date
		datetime_show = datetime.datetime(start_date.year, start_date.month, start_date.day) 
		datetime_show_start = datetime_show.replace(hour=self.show_start_time.hour, minute=self.show_start_time.minute)
		datetime_show_end = datetime_show.replace(hour=self.show_end_time.hour, minute=self.show_end_time.minute)

		timings = {} 
		timings['slot_start_time'] = datetime_show_start - self.show.get_in_dur
		timings['slot_end_time'] = datetime_show_end - self.show.get_out_dur 
		timings['slot_duration'] = timings['slot_start_time'] - timings['slot_end_time']
		return timings 

	@property
	def event(self):
		return self.show.event 

	def __str__(self):
		return 'Slot preference ' + str(self.slot_preference) + ' for ' + str(self.show.show_title) + ' (' + str(self.show.company) + ', ' + str(self.venue.title) + ')'

class Comment(models.Model):
	show = models.ForeignKey(Show, on_delete=models.CASCADE, null=True)
	author = models.ForeignKey('people.Person', on_delete=models.CASCADE)
	date = models.DateField() 
	comment = models.TextField()  
	publish_date = models.DateTimeField()

	def __str__(self):
		return 'Comment from ' + self.author + ' on ' + self.publish_date

class Vote(models.Model):
	show = models.ForeignKey(Show, on_delete=models.CASCADE, null=True)
	score = models.CharField(
		choices = (
			('A+', 'Amazing'),
			('A', 'Bit fine actually')
		),
		default='A',
		max_length=30,
	)
	subject = models.CharField(max_length=180)
	status = models.CharField(
		choices = (
			('M', 'Moral'),
			('T', 'Technical'),
			('A', 'Artistic'),
			('N', 'Note')
		),
		default='N',
		max_length=10
	)
	comment = models.TextField()
	author = models.ForeignKey('people.Person', on_delete=models.CASCADE)

	def __str__(self):
		return self.score + ' by ' + self.author 


class Invoice(models.Model):
	company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)
	show = models.ForeignKey(Show, null=True, blank=True, on_delete=models.CASCADE)
	person = models.ForeignKey('people.Person', null=True, blank=True, on_delete=models.CASCADE)

	invoice_amount = models.DecimalField(null=True, decimal_places=2, max_digits=10)
	invoice_status = models.CharField(max_length=20, choices=(
			('DRAFT', 'Draft'),
			('SENT', 'Sent to recipient'),
			('PAID', 'Paid by recipient')
		), default='DRAFT')
	invoice_date = models.DateField(null=True)
	xero_reference = models.CharField(max_length=50, blank=True)

