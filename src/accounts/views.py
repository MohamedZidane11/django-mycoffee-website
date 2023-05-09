from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from .models import UserProfile
import re

# Create your views here.
def signin(request):
    if request.method == 'POST' and 'btnsignin' in request.POST:

        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if 'rememberme' not in request.POST:
                request.session.set_expiry(0)
            auth.login(request, user)
            #messages.info(request, "You are now logged in")
        else:
            messages.error(request, "Your username or password is incorrect")

        return redirect('accounts:signin')
    else:
        return render(request, "accounts/signin.html")


def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect('pages:index')


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
        is_added = None

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
                            userprofile = UserProfile\
                                (user=user, address1=address1,
                                 address2=address2, city=city,
                                 state=state, zip_number=zip_number)
                            userprofile.save()

                            # Clean fields
                            fname = ''
                            lname = ''
                            address1 = ''
                            address2 = ''
                            city = ''
                            state = ''
                            zip_number = ''
                            email = ''
                            username = ''
                            password = ''
                            terms = None

                            # Success message
                            messages.success(request, 'Your account is created successfully')
                            is_added = True
                        else:
                            messages.error(request, "Invalid email")
            else:
                messages.error(request, 'You must agree on the terms')
        else:
            messages.error(request, 'Check empty fields')

        return render(request, "accounts/signup.html",{
            'fname': fname,
            'lname': lname,
            'address1': address1,
            'address2': address2,
            'city': city,
            'state': state,
            'zip': zip_number,
            'email': email,
            'username': username,
            'password': password,
            'is_added': is_added
        })
    else:
        return render(request, "accounts/signup.html")


def profile(request):
    if request.method == 'POST' and 'btnSave' in request.POST:
        if request.user is not None and request.user.id != None:
            userprofile = UserProfile.objects.get(user=request.user)
            if request.POST['fname'] and request.POST['lname'] and request.POST['address1'] and request.POST['address2'] and\
                request.POST['city'] and request.POST['state'] and request.POST['zip'] and request.POST['email'] and\
                request.POST['username'] and request.POST['password']:
                request.user.first_name = request.POST['fname']
                request.user.last_name = request.POST['lname']
                userprofile.address1 = request.POST['address1']
                userprofile.address2 = request.POST['address2']
                userprofile.city = request.POST['city']
                userprofile.state = request.POST['state']
                userprofile.zip_number = request.POST['zip']
                #request.user.email = request.POST['email']
                #request.user.username = request.POST['username']
                if not request.POST['password'].startswith('pbkdf2_sha256$'):
                    request.user.set_password(request.POST['password'])
                request.user.save()
                userprofile.save()
                auth.login(request, request.user)
                messages.success(request, 'your data has been saved')
            else:
                messages.error(request, 'Check your values and elements')
        return redirect('accounts:profile')
    else:
        #if request.user.id == None: return redirect('pages:index')

        if request.user is not None:
            context = None
            if not request.user.is_anonymous:
                userprofile = UserProfile.objects.get(user=request.user)

                context = {
                    'fname': request.user.first_name,
                    'lname': request.user.last_name,
                    'address1': userprofile.address1,
                    'address2': userprofile.address2,
                    'city': userprofile.city,
                    'state': userprofile.state,
                    'zip': userprofile.zip_number,
                    'email': request.user.email,
                    'username': request.user.username,
                    'password': request.user.password,
                }
            return render(request, "accounts/profile.html", context)
        else:
            return redirect('accounts:profile')

