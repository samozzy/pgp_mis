from django.contrib import messages 
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.urls import reverse, reverse_lazy

from people.models import Person 

def put_user_in_group(user, group_name='company'):
	the_group = Group.objects.filter(name=group_name).first() 
	if the_group: 
		the_group.user_set.add(user)
	else:
		message_string = "The user group - " + str(group_name) + " - does not exist. Please contact an IT administrator immediately."
		messages.add_message(self.request, messages.ERROR, message_string)

def get_user_profile(user):
	p = Person.objects.filter(site_user = user).first()
	# objects.get() will raise an exception, and we want to handle the fail ourselves
	if p:
		return p 
	else:
		return False

def user_can_make_show_offer(user):
	return user.has_perm('programming.dir_can_make_offer')

def user_can_admin_show(user):
	return user.has_perm('programming.dir_can_administrate_shows')

def user_can_make_application_offer(user):
	return user.has_perm('staffing.dir_can_accept_application')

def user_is_director(user):
	return user.groups.filter(name='director').exists()

class MISUserMixin:
	# Add the user profile to the context and work out whether this user is feasibly a director (to gain access to extra special things)
	def get_context_data(self, **kwargs):
		context = super().get_context_data()
		context['user_profile'] = get_user_profile(self.request.user)
		if context['user_profile']:
			if context['user_profile'].person_type == 'STAFF':
				if user_is_director(self.request.user):
					context['user_is_director'] = True 
				elif user_can_make_show_offer(self.request.user) \
					or user_can_admin_show(self.request.user) \
					or user_can_make_application_offer(self.request.user):
					context['user_is_director'] = True 
		return context 

class MISPermissionMixin(MISUserMixin, LoginRequiredMixin):
	''' 
	Permissions mixin that activates object-level permissions based on user status (should be applied to - almost* - every view).
	Test if the user is logged in, and if they are either a volunteer or authorised company member
	The broad rules are:
		1. All users must be authenticated 
		2. Staff get at least view access to all the things
		3. Companies only get (at least) view access to the programming app 

	For CRUD operations (including access to the form), we use the PermissionRequiredMixin and individual per-view permission checks 
	Requirements: To use the PermissionRequiredMixin, manual setup of either Group- or User-level permissions is needed
	By default, only superusers have all the permissions. 
	The recommended method is to make groups, assign the permissions to the groups, and then assign the users to the groups

	* Views this mxiin should not be applied to:
		- User registration (there is no login requirement)
	'''

	def dispatch(self, *args, **kwargs):
		app_name = self.request.resolver_match._func_path.split('.')[0]
		success = False 
		if self.request.user.is_authenticated:
			# Check that the user has a valid user_profile instance before we can do literally anything
			p = get_user_profile(self.request.user)
			if not p :
				if reverse_lazy('people:personSetUp') == self.request.path:
					# Don't redirect if we're legitimately landing on the setup page
					success = True 
				else: 
					messages.add_message(self.request, messages.ERROR, "You haven't finished setting up your profile, and you need to do that to continue.")
					return redirect(reverse_lazy('people:personSetUp'))

			if app_name == 'programming' or app_name == 'people':
				# Company members can see their own shows and their own user profiles.
				# TODO: Expand this so that they can access other people for their company 
				if app_name == 'programming':
					if p.person_type == 'COMPY':
						the_object = None 
						if hasattr(self, 'get_object'):
							# If the page is relating to an object, we can use it directly
							the_object = self.get_object()
						elif hasattr(self, 'get_queryset'):
							# If not, we'll see if it's got a queryset, and take the first item 
							# This is permissable on the assumption that the user will have an all or nothing access to the queryset
							the_object = self.get_queryset().first() 

						if the_object:
							if hasattr(the_object, 'show'): 
								# If this is an object attached to a show (eg a Slot), get the show
								the_object = the_object.show 
							elif type(the_object).__name__ == 'Show':
								# Confirm it is in fact a show before we try and do anything with it 
								the_object = the_object
							else:
								# If we can't get a show out of the object, sack it off 
								# (It still needs to exist though)
								the_object = False
								success = True 
							if the_object:
								if the_object.lead_contact and the_object.lead_contact == p \
								or the_object.company and the_object.company.lead_contact == p: 
									success = True 
								else:
									messages.add_message(self.request, messages.ERROR, "This is not one of your shows, so you don't have access to it. Please get in touch if you think this is an error.")
									raise PermissionDenied
						else:
							success = True 
					elif p.person_type == 'STAFF':
						success = True 
				elif app_name == 'people':
					if type(self.get_object()).__name__ == 'Person':
						if self.get_object().site_user == self.request.user or user_is_director(self.request.user):
							success = True 
						else: 
							messages.add_message(self.request, messages.ERROR, "You cannot access someone else's user profile. Please get in touch if you think this is an error.")
							raise PermissionDenied
				else: 
					success = True 
			elif app_name == 'staffing' and not user_is_director(self.request.user):
				# Within the staffing app, much of the permissions are handled by director-only-ness. 
				# However, staff need to be able to edit their applications and offers, so... 
				the_object = None 
				if hasattr(self, 'get_object'):
					# If the page is relating to an object, we can use it directly
					the_object = self.get_object()
				elif hasattr(self, 'get_queryset'):
					# If not, we'll see if it's got a queryset, and take the first item 
					# This is permissable on the assumption that the user will have an all or nothing access to the queryset
					the_object = self.get_queryset().first() 

				if the_object:
					if hasattr(the_object, 'person'): 
						# If this is an object attached to a person (eg an Application), get the person
						the_object = the_object.person 
					elif hasattr(the_object, 'application'):
						# Offers don't have a person, so we can get it through the Application
						the_object = the_object.application.person 
					elif type(the_object).__name__ == 'Person':
						# Confirm it is in fact a person before we try and do anything with it 
						the_object = the_object
					else:
						# If we can't get a person out of the object, sack it off 
						# (It still needs to exist though)
						the_object = False
						success = True 
					if the_object and the_object == get_user_profile(self.request.user):
						success = True 
					else:
						messages.add_message(self.request, messages.ERROR, "This relates to someone else's personal details, so you don't have access to it. Please get in touch if you think this is an error.")
						raise PermissionDenied
			else: 
				if p.person_type != 'STAFF':
					# If it's neither the programming or people apps, assume it's staff only and shoo everyone else away
					messages.add_message(self.request, messages.ERROR, "This is a staff-only area of the site. Please get in touch if you think this is an error.")
					raise PermissionDenied
				else:
					success = True 
			if success == True:
				print('SUCCESS')
				return super(MISPermissionMixin, self).dispatch(*args, **kwargs) 
			else:
				messages.add_message(self.request, messages.ERROR, str(get_user_profile(self.request.user)))
				raise PermissionDenied
		else:
			# If the user is not authenticated, let LoginRequiredMixin take over 
			# Equally, if there's no object, we don't need to do object-based tests
			return super(MISPermissionMixin, self).dispatch(*args, **kwargs)