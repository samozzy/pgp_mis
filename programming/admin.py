from django.contrib import admin
from django.db import models
from .models import * 
from people.models import Person, PersonShow
from django.forms import CheckboxSelectMultiple
# Register your models here

def get_user_profile(u, **kwargs):
	try:
		Person.objects.get(site_user=u) 
	except Person.DoesNotExist:
		return None 


class VenueAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'parent_venue')

class SlotInline(admin.StackedInline):
	model = Slot 
	extra = 1

	fields = (
		('venue', 'show_start_time', 'show_end_time'),
		('slot_preference', 'week', 'has_preview'),
		('slot_price', 'slot_guarantee', 'box_office')
	)

class PersonShowInline(admin.StackedInline):
	model = PersonShow 
	extra = 1 

class OfferInline(admin.StackedInline):
	model = Offer
	extra = 0 

class VoteInline(admin.TabularInline):
	model = Vote 
	extra = 0

class CommentInline(admin.TabularInline):
	model = Comment 
	extra = 0

class CompanyAdmin(admin.ModelAdmin):
	formfield_overrides = {
		models.ManyToManyField: {'widget': CheckboxSelectMultiple},
	}

	# Permissions
	def has_view_permission(self, request, obj=None):
		if request.user.is_authenticated:
			if get_user_profile(request.user):
				p = get_user_profile(request.user)
				if p.person_type == 'STAFF':
					return True 
				elif p.person_type == 'COMPY':
					# If the person is a company member and the show is in their show list, let them see it
					return True 
				else:
					return False 
			else:
				return False 
		else:
			return False 

	def has_module_permission(self, request):
		return True 

class ShowAdmin(admin.ModelAdmin):
	list_display = ('__str__', 'status', 'event')

	fieldsets = (
		(None, {
			'fields': (
				('show_title', 'event', 'status'),
				('company', 'lead_contact', 'level'),
				'via_link',
				'poster'
			)
		}),
		('Marketing', {
			'fields': (
				'copy_short',
				'copy_long')
		}),
		('Long Answer Questions', {
			'fields': (
				'outline',
				'motivation',
				'funding')
			}),
		('Backstage', {
			'fields': (
				('cast_size', 'crew_size'),
				'tech_outline',
				'set_outline')
			}),
		('Timings', {
			'fields': (
				('get_in_dur', 'show_duration', 'get_out_dur'),
				)
			}),
		)
	inlines = [ SlotInline, VoteInline, CommentInline, OfferInline, PersonShowInline ]

	# Permissions
	def has_view_permission(self, request, obj=None):
		if get_user_profile(request.user):
			p = get_user_profile(request.user)
			if p.person_type == 'STAFF':
				return True 
			elif p.person_type == 'COMPY':
				# If the person is a company member and the show is in their show list, let them see it
				for companies in p.company:
					for s in companies.get_shows():
						if s == obj:
							return True 
						else:
							return False 
			else:
				return False 
		else:
			return False 

class WeekInline(admin.TabularInline):
	model = Week 

class EventAdmin(admin.ModelAdmin):
	inlines = [ WeekInline ] 

admin.site.register(Show, ShowAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Venue, VenueAdmin)