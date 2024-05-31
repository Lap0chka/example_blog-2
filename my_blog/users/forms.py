from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User



class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'image', 'username', 'email',)

    def save(self, commit=True):
        image = self.cleaned_data['image']
