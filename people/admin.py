from django.contrib import admin
from .models import * 

# Register your models here.

class PersonShowInline(admin.StackedInline):
	model = PersonShow 
	extra = 0 

class ContactDetailsInline(admin.StackedInline):
	model = ContactDetail 
	extra = 0

	fields = (
		'contact_reference',
		('email_primary', 'email_secondary'),
		('mobile_number', 'phone_number'),
		('post_point', 'building_name', 'building_number'),
		'street_name',
		('city', 'region'),
		('country', 'post_code')
	)

class PersonAdmin(admin.ModelAdmin):
	fields = (
		('site_user', 'person_type'),
		('forename', 'middle_name', 'surname'),
		'pronouns',
		'photo',
		('medical_info', 'allergies')
	)
	inlines = [ ContactDetailsInline, PersonShowInline ]


admin.site.register(Person, PersonAdmin)
admin.site.register(Allergy)