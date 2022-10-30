from django.contrib.auth import authenticate, login 
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.http import HttpResponseRedirect

from people.forms import UserRegistrationForm

class UserRegisterView(SuccessMessageMixin, CreateView):
  template_name = 'register.html'
  success_url = reverse_lazy('programming:programmingDashboard')
  form_class = UserRegistrationForm
  success_message = "You've registered successfully."

  def form_valid(self, form):
    user = form.save() 
    username = user.username
    password = form.cleaned_data['password1']
    user = authenticate(username=username, password=password)
    login(self.request, user)
    return HttpResponseRedirect(reverse_lazy('people:personSetUp'))
