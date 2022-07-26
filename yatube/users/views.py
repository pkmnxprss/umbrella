from django.views.generic import CreateView

# function allows you to get the URL given the "name" parameter of the path() function
from django.urls import reverse_lazy
from .forms import CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("login")  # where login is the "name" parameter in path()
    template_name = "signup.html"
