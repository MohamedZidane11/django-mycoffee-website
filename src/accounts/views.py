from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .models import userProfile
import re

# Create your views here.
def signin(request):
    if request.method == 'POST' and 'btnsignin' in request.POST:
        messages.info(request, "This is POST and btn")
        return redirect('accounts:signin')
    else:
        return render(request, "accounts/signin.html")


def signup(request):
    if request.method == 'POST' and 'btnsignup' in request.POST:

        # variables for fields
        fname = None
        lname = None
        address1 = None
        address2 = None
        city = None
        state = None
        zip_number = None
        email = None
        username = None
        password = None
        terms = None

        # get values from the form
        if 'fname' in request.POST: fname = request.POST['fname']
        else: messages.error(request, 'Error in first name')
        if 'lname' in request.POST: lname = request.POST['lname']
        else: messages.error(request, 'Error in last name')
        if 'address1' in request.POST: address1 = request.POST['address1']
        else: messages.error(request, 'Error in address1')
        if 'address2' in request.POST: address2 = request.POST['address2']
        else: messages.error(request, 'Error in address2')
        if 'city' in request.POST: city = request.POST['city']
        else: messages.error(request, 'Error in city')
        if 'state' in request.POST: state = request.POST['state']
        else: messages.error(request, 'Error in state')
        if 'zip' in request.POST: zip_number = request.POST['zip']
        else: messages.error(request, 'Error in zip number')
        if 'email' in request.POST: email = request.POST['email']
        else: messages.error(request, 'Error in email')
        if 'username' in request.POST: username = request.POST['username']
        else: messages.error(request, 'Error in username')
        if 'password' in request.POST: password = request.POST['password']
        else: messages.error(request, 'Error in password')
        if 'terms' in request.POST: terms = request.POST['terms']

        # check values
        if fname and lname and address1 and address2 and city and state and zip_number and email and username and password:
            if terms == 'on':
                # Check if username is taken
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'This username is taken')
                else:
                    # Check if email is taken
                    if User.objects.filter(email=email).exists():
                        messages.error(request, 'This email is taken')
                    else:
                        patt = "^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
                        if re.match(patt, email):
                            # Add new user
                            user = User.objects.create_user\
                                (first_name=fname, last_name=lname,
                                 email=email, username=username,
                                 password=password)
                            user.save()
                            # Add new user profile
                            userprofile = userProfile\
                                (user=user, address1=address1,
                                 address2=address2, city=city,
                                 state=state, zip_number=zip_number)
                            userprofile.save()
                            # Success message
                            messages.success(request, 'Your account is created successfully')
                        else:
                            messages.error(request, "Invalid email")
            else:
                messages.error(request, 'You must agree on the terms')
        else:
            messages.error(request, 'Check empty fields')

        return redirect('accounts:signup')
    else:
        return render(request, "accounts/signup.html")


def profile(request):
    if request.method == 'POST' and 'btnprofile' in request.POST:
        messages.info(request, "This is POST and btn")
        return redirect('accounts:profile')
    else:
        return render(request, "accounts/profile.html")
