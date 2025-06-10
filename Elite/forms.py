from django import forms
from .models import Player, PerformanceStat, Scout, Team
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class PlayerAddForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'age', 'nationality', 'position', 'current_worth', 'height', 'date_of_birth', 'team']


class PlayerUpdateForm(forms.ModelForm):
    class Meta:
        model = Player
        exclude = ['name', 'nationality', 'date_of_birth']

class ScoutForm(forms.ModelForm):
    class Meta:
        model = Scout
        fields = '__all__'

class PerformanceStatAddForm(forms.ModelForm):
    class Meta:
        model = PerformanceStat
        fields = ['matches_played', 'tries_scored', 'successful_tackles', 'overall_rating']

class PerformanceStatUpdateForm(forms.ModelForm):  
    class Meta:
        model = PerformanceStat
        exclude = ['player']

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    organization = forms.CharField(max_length=100, required=True, help_text="Enter your organization name")
    role = forms.ChoiceField(choices=[("head scout", "Head Scout"), ("assistant", "Assistant")])
    teams = forms.ModelMultipleChoiceField(queryset=Team.objects.all(), widget=forms.SelectMultiple)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "organization", "role", "teams"]

    def save(self, commit=True):
         user = super().save(commit=False)
         user.email=self.cleaned_data["email"]
         if commit:
             user.save()
             Scout.objects.create(
                 user=user, 
                 organization=self.cleaned_data['organization']
                 )
         return user


class TeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['coach', 'league', 'logo']


class DonationForm(forms.Form):
    phone = forms.CharField(label="Mpesa Phone Number", max_length=13)
    amount = forms.DecimalField(label="Amount (KES)", min_value=1)


