from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import balance, UserProfile
from .forms import CurrencyForm, WalletForm, UserForm, ProfileForm, UserForm1
from django.contrib.auth.models import User
# Create your views here.

from django.contrib.auth.decorators import login_required
import urllib.request
import json
from decimal import Decimal

URL = "https://openexchangerates.org/api/latest.json?app_id=ec5161e8e9cc413ebe42bd0aaf56b957"

@login_required
def profile(request):
	if request.user.is_authenticated:
		user_profile = UserProfile.objects.get(user=request.user)
		user = balance.objects.get(user=request.user)
	if request.POST:
		userform = UserForm1(request.POST, instance = request.user)
		profileform = ProfileForm(request.POST, instance = user_profile)
		if userform.is_valid() and profileform.is_valid():
			user = userform.save()
			profile = profileform.save(commit=False)
			profile.user = user

		if 'picture' in request.FILES:
			profile.picture = request.FILES['picture']
			profile.save()
			return redirect('/accounts/profile/', messages.success(request, 'Profile Successfully Updated.', 'alert-success'))
		else:
			print(userform.errors, profileform.errors)
			return redirect('/accounts/profile/', messages.error(request, 'Profile is not Valid', 'alert-danger'))
	else:
		form1 = UserForm1(instance = request.user)
		form2 = ProfileForm(instance = user_profile)
	return render(request,'profile.html', {'form1':form1, 'form2': form2,'balance': user.balance})


def registerView(request):
	if request.method =='POST':
		form1 = UserForm(request.POST)
		form2 = ProfileForm(request.POST,request.FILES)
		if form1.is_valid():
			user = form1.save()
			login(request, user)
			if request.user.is_authenticated:
				UserProfile.objects.create(user= request.user)
				instance = balance()
				instance.user = request.user
				instance.balance = int(100)
				#instance = balance.objects.create(request.user, balance = d)
				instance.save()
			return redirect("login")
		else:
			print(form1.errors, form2.errors)
	else:
		form1 = UserForm()
		form2 = ProfileForm()
	return render(request, 'registration/register.html', {'form1': form1, 'form2':form2})

def get_json(url):
    try:
        html = urllib.request.urlopen(url)
    except urllib.error.URLError as e:
        return redirect('/conversion', messages.error(request, 'Something C', 'alert-danger'))
    except urllib.error.HTTPError as e:
        return redirect('/conversion', messages.error(request, 'Something B', 'alert-danger'))
    raw_json = html.read().decode('utf-8')
    forex_json = json.loads(raw_json)
    return forex_json

@login_required
def dashboardView(request):
	if request.user.is_authenticated:
		user = balance.objects.get(user=request.user)

	if request.POST.get('send', False):
		form1 = WalletForm(request.POST)
		if form1.is_valid():
			try:
				username = form1.cleaned_data["username"]
				print(username)
				amount = form1.cleaned_data["amount"]
				senderUser = User.objects.get(username=request.user.username)
				print(senderUser)
				receiverUser = User.objects.get(username=username)
				print(receiverUser)
				sender = balance.objects.get(user = senderUser)
				if (sender.balance <= 10):
					return redirect('/accounts', messages.success(request, 'Insufficient Amount', 'alert-danger'))
				else:
					print(sender)
					receiver = balance.objects.get(user = receiverUser)
					print(receiver)
					sender.balance = sender.balance - int(amount)
					receiver.balance = receiver.balance + int(amount)
					sender.save()
					receiver.save()
					return redirect('/accounts', messages.success(request, 'Transaction Success', 'alert-success'))
			except Exception as e:
				print(e)
				return redirect('/accounts', messages.success(request, 'Transaction Failure, Please check and try again', 'alert-danger'))
	else:
		form1 = WalletForm()

	if request.POST.get('check', False):
		form = CurrencyForm(request.POST)
		if form.is_valid():
			forex_data = get_json("https://openexchangerates.org/api/latest.json?app_id=ec5161e8e9cc413ebe42bd0aaf56b957")
			amount_curr = request.POST['amount_curr']
			base_curr = request.POST['base_curr']
			new_curr = request.POST['new_curr']
			print(amount_curr)
			print(base_curr)
			print(new_curr)
			try:
				conv_rate = Decimal(forex_data['rates'][new_curr]) * Decimal(1) / Decimal(forex_data['rates'][base_curr])
				t_amount = Decimal(amount_curr) * conv_rate
				amt = "{:.2f}".format(t_amount)
				result = new_curr + " " + amt
				print(result)
				return render(request,'dashboard.html', {'balance': user.balance, 'form':form, 'form1':form1, 'result':result})
			except KeyError as e:
				return redirect('/accounts', messages.error(request, 'Invalid Currency', 'alert-danger'))
	else:
		form = CurrencyForm()
	return render(request, 'dashboard.html', {'form':form, 'form1':form1, 'balance': user.balance})
