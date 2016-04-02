from django import forms
from django.contrib.auth import get_user_model


User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


# cleaning up the data of the username and the password and validating the
# credentials.
    def clean_username(self):
        # Getting the data from the form that is being passed through then check
        # whether the user exists. If the user does not exist it will raise a
        # validation error prompting the user to check his credentials.

        username = self.cleaned_data.get("username")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Are you sure you are registered?")
        return username
    def clean_password(self):
        username = self.cleaned_data.get("username")

        # getting the password data that is being passed through and checking
        # if the password is valid. If the password is not valid but the user exists,
        # a validation error will be raised a prompting the user to check his
        # password credentials. Else if the user does not exist it will pass since
        # since it was checked above and finally it will return the password

        password = self.cleaned_data.get("password")
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            user = None
        if user is not None and not user.check_password(password):
             raise forms.ValidationError("invalid password")
        elif user is None:
            pass
        else:
            return password

class RegistrationForm(forms.ModelForm):
    # Register a new user and have them confirm their chosen password
    email = forms.EmailField(label = 'Your Email')
    password1 = forms.CharField(label = 'Password', widget=forms.PasswordInput())
    password2 = forms.CharField(label = 'Password Confirmation', widget=forms.PasswordInput())
    # Takes from the model of User which is defined above as a django function.
    class Meta:
        model = User
        # fields from the models that we would like to display in addition to password
        # and password confirmation.
        fields = ['username', 'email']


    def clean_password2(self):
        # Checking the second password against the first by cleaning the data and then
        # validating whether they match. If not, raises a validation error.
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return password2


    def clean_email(self):

        email = self.cleaned_data.get("email")
        user_count = User.objects.filter(email=email).count()
        if user_count > 0:
             raise forms.ValidationError("This email has already been registered. Please check and try again")
        return email


    # saving the new user information.
    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        # user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user










