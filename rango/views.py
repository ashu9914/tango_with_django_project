from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category
from rango.models import Page
from rango.forms import CategoryForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from rango.models import UserProfile
from rango.forms import UserForm, UserProfileForm
from datetime import datetime

def register(request):
 # A boolean value for telling the template
 # whether the registration was successful.
 # Set to False initially. Code changes value to
 # True when registration succeeds.
 registered = False

 # If it's a HTTP POST, we're interested in processing form data.
if request.method == 'POST':
 # Attempt to grab information from the raw form information.
 # Note that we make use of both UserForm and UserProfileForm.
 user_form = UserForm(request.POST)
 profile_form = UserProfileForm(request.POST)

 # If the two forms are valid...
if user_form.is_valid() and profile_form.is_valid():
 # Save the user's form data to the database.
 user = user_form.save()

 # Now we hash the password with the set_password method.
 # Once hashed, we can update the user object.
 user.set_password(user.password)
 user.save()

 # Now sort out the UserProfile instance.
 # Since we need to set the user attribute ourselves,
 # we set commit=False. This delays saving the model

 # until we're ready to avoid integrity problems.
 profile = profile_form.save(commit=False)
 profile.user = user

 # Did the user provide a profile picture?
 # If so, we need to get it from the input form and
 #put it in the UserProfile model.
if 'picture' in request.FILES:
 profile.picture = request.FILES['picture']

 # Now we save the UserProfile model instance.
 profile.save()

 # Update our variable to indicate that the template
 # registration was successful.
 registered = True
else:
 # Invalid form or forms - mistakes or something else?
 # Print problems to the terminal.
 print(user_form.errors, profile_form.errors)
else:
# Not a HTTP POST, so we render our form using two ModelForm instances.
# These forms will be blank, ready for user input.
user_form = UserForm()
profile_form = UserProfileForm()

# Render the template depending on the context.
return render(request),
  'rango/register.html',
  context = {'user_form': user_form,
  'profile_form': profile_form,
  'registered': registered})

def visitor_cookie_handler(request, response):
# Get the number of visits to the site.
# We use the COOKIES.get() function to obtain the visits cookie.
# If the cookie exists, the value returned is casted to an integer.
# If the cookie doesn't exist, then the default value of 1 is used.
    visits = int(request.COOKIES.get('visits', '1'))
last_visit_cookie = request.COOKIES.get('last_visit', str(datetime.now()))
last_visit_time = datetime.strptime(last_visit_cookie[:-7],
'%Y-%m-%d %H:%M:%S')
# If it's been more than a day since the last visit...
if (datetime.now() - last_visit_time).days > 0:
visits = visits + 1
# Update the last visit cookie now that we have updated the count
response.set_cookie('last_visit', str(datetime.now()))
else:
# Set the last visit cookie
response.set_cookie('last_visit', last_visit_cookie)
# Update/set the visits cookie
response.set_cookie('visits', visits)
