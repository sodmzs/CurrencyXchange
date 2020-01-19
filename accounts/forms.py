from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile
from django.forms import ModelForm

class WalletForm(forms.Form):
	username = forms.ModelChoiceField(queryset=User.objects.all(), empty_label=None, widget=forms.Select(attrs={'class':'form-control'}))
	amount = forms.IntegerField()

class CurrencyForm(forms.Form):
	amount_curr = forms.IntegerField()
	base_curr = forms.CharField(max_length=5)
	new_curr = forms.CharField(max_length=5)

class UserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username']

class UserForm1(UserChangeForm):
	class Meta:
		model = User
		fields = ['username', 'password']

class ProfileForm(ModelForm):
	picture = forms.ImageField(widget=forms.FileInput)
	class Meta:
		model = UserProfile
		fields = ['website','picture']


