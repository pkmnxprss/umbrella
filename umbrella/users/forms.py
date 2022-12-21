from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model


User = get_user_model()


# Create our own class for the registration form (inheritor of the predefined UserCreationForm class)
class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User  # model that the created form is associated with

        # Fields that should be visible in the form and their order
        fields = ("first_name", "last_name", "username", "email")
