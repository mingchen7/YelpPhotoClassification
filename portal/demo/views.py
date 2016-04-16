from django.shortcuts import render
from django.template import loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from demo.models import User, Business, Rating
import datetime
import hashlib

# Create your views here.

def user(request):
	context = {
		'id': 'user'
	}	
	return render(request, 'demo/user.html', context)	

def business(request):
	context = {'id': 'business'}
	return render(request, 'demo/business.html', context)

def detail(request):
	context = {}
	return render(request, 'demo/detail.html', context)

def recommendation(request):
	context = {}
	return render(request, 'demo/recommendation.html', context)

def register(request):
	try:
		# register a new user
		sys_time = str(datetime.datetime.now())
		hash_md5 = hashlib.md5(sys_time)		
		hash_pwd = hashlib.md5(request.POST['password'])

		user_id = hash_md5.hexdigest()
		username = request.POST['username']
		email = request.POST['email']		
		encoded_pwd = hash_pwd.hexdigest()

		print user_id
		print request.POST['username']
		print request.POST['email']
		print request.POST['password']
		print encoded_pwd
		user = User(user_id, username, email, encoded_pwd)
		user.save()		

	except KeyError:
		render(request, 'demo/user.html', {
			'error_message': "Username has already existed!"
			})

	# redirect back to businesses page
	else:
		return HttpResponseRedirect(reverse('demo:business'))

