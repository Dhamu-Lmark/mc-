from email.message import EmailMessage
import requests
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Users, ContactSubmission


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # Check if user with given username or email already exists
        if Users.objects.filter(username=username).exists() or Users.objects.filter(email=email).exists():
            messages.error(request, 'Username or Email is already taken')
            return redirect('register')
        else:
            # Create new user
            user = Users.objects.create(username=username, email=email, password=password)
            user.save()
            messages.success(request, 'Registration successful. You can now log in.')
            return redirect('login')
    return render(request, 'register.html')


def dashboard(request):
    logged_in_user = request.session.get('logged_in_user')
    if logged_in_user:
        return render(request, 'dashboard.html', {'username': logged_in_user})
    else:
        return redirect('login')

def home(request):
    return render(request, 'home.html')

def Account_Manager(request):
    return render(request, 'Account Manager.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # Check if user with given email and password exists
        user = Users.objects.filter(email=email, password=password).first()
        if user:
            request.session['logged_in_user'] = user.username  # Set username as logged-in user
            messages.success(request, 'Login successful')
            return redirect('demo')
        else:
            messages.error(request, 'Invalid email or password')
            return redirect('login')
    return render(request, 'login.html')


def logout(request):
    if 'logged_in_user' in request.session:
        del request.session['logged_in_user']
        messages.success(request, 'Logout successful')
    return redirect('home')

def Trade_Copier(request):
    return render(request, 'Trade Copier.html')

def Blog(request):
    return render(request, 'Blog.html')

def Pricing(request):
    return render(request, 'Pricing.html')

def Contact(request):
    return render(request, 'Contact.html')

# def Contact(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         subject = request.POST.get('subject')
#         message = request.POST.get('message')
#
#         # Save the contact submission to the database
#         ContactSubmission.objects.create(name=name, email=email, subject=subject, message=message)
#
#         # Optionally, you can send a confirmation email to the user
#
#         return HttpResponse("Thank you for your submission. We'll get back to you shortly.")
#
#     return render(request, 'Contact.html')


# views.py

from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Users
from .utils import generate_token




def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = Users.objects.filter(email=email).first()
        if user is not None:
            # Generate a password reset token
            token = generate_token()

            # Save the token to the user model
            user.reset_password_token = token
            user.save()

            # Construct password reset URL
            reset_url = request.build_absolute_uri(
                f'/reset-password/{user.id}/{token}/'
            )

            # Send password reset email
            subject = 'Password Reset Request'
            message = render_to_string('password_reset_email.html', {
                'reset_url': reset_url
            })
            sender_email = settings.EMAIL_HOST_USER  # Change to your email address
            send_mail(subject, message, sender_email, [email])

            messages.success(request, 'An email has been sent with instructions to reset your password.')
            return redirect('login')
        else:
            messages.error(request, 'There is no user with that email address.')
            return render(request, 'forget password.html')
    return render(request, 'forget password.html')


# views.py



from django.contrib import messages

def reset_password(request, user_id, token):
    user = Users.objects.filter(id=user_id, reset_password_token=token).first()
    if user is not None:
        if request.method == 'POST':
            password = request.POST.get('password')

            # Update the user's password
            user.password = password  # Assuming 'password' is plain text, which is not recommended

            # Clear the reset_password_token
            user.reset_password_token = None

            # Save the updated user
            user.save()

            messages.success(request,
                             'Your password has been reset successfully. You can now log in with your new password.')
            return redirect('login')
        return render(request, 'reset_password.html')
    else:
        messages.error(request, 'The password reset link is invalid or has expired.')
        return redirect('login')



from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.contrib import messages
from .models import Notify
from django.db import IntegrityError


# def demo(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         if email:
#             try:
#                 # Try to save the email to the database
#                 subscriber, created = Notify.objects.get_or_create(email=email)
#                 if created:
#                     # Send a confirmation email to the user
#                     subject = 'User Confirmation'
#                     message = '''<html><body>
#     <p>Dear User,</p>
#
#     <p>Thank you for joining Master Copier Tools! We are excited to have you on board.</p>
#
#     <p>You will receive regular updates and notifications about our latest products, promotions, and news.</p>
#
#     <p>If you have any questions or need further assistance, feel free to contact us at <a href="mailto:info@example.com">info@example.com</a>.</p>
#
#     <p>Best regards,<br>The Master Copier Tools Team.</p>
#     </body></html>'''
#                     from_email = 'dhamotharan2107@gmail.com'  # Sender's email address
#                     to_email = [email]  # List of recipients
#
#                     email = EmailMessage(subject, message, from_email, to_email)
#                     email.content_subtype = "html"  # Set email content type to HTML
#                     email.send()
#
#                     messages.success(request, 'Thank you for subscribing! We have sent you a confirmation email.')
#                 else:
#                     messages.info(request,
#                                   'You are already subscribed.')  # Display a message if email is already subscribed
#             except IntegrityError:
#                 messages.error(request, 'An error occurred while processing your request. Please try again later.')
#
#             return redirect('demo')  # Redirect to the same page after form submission
#     return render(request, 'demo.html')

def demo(request):
    logged_in_user = request.session.get('logged_in_user')
    if logged_in_user:
        return render(request, 'demo.html', {'username': logged_in_user})
    else:
        return redirect('login')


from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Account

from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from .models import Account  # Import the Account model


# Rename the function to avoid naming conflict
def account_view(request):
    logged_in_user = request.session.get('logged_in_user')

    # If the user is logged in
    if logged_in_user:
        # Retrieve all accounts from the Account model
        accounts = Account.objects.all()

        # Render the 'Account.html' template with the accounts data
        return render(request, 'Account.html', {'accounts': accounts})

    # If the user is not logged in, redirect to the login page
    else:
        return redirect('login')


def Add_Account(request):
    logged_in_user = request.session.get('logged_in_user')

    # Redirect to login page if not logged in
    if not logged_in_user:
        return redirect('login')

    # Initialize the brokers list
    brokers = []

    if request.method == 'POST':
        # Retrieve POST data
        account_type = request.POST.get('accountType')
        description_name = request.POST.get('descriptionName')
        account_number = request.POST.get('accountNumber')
        password = request.POST.get('password')
        broker_name = request.POST.get('broker')
        server_name = request.POST.get('server')

        # Validate user input against account details from the API
        api_url = 'http://localhost:3000/api/accountDetails'
        response = requests.get(api_url)

        # Initialize validation flag
        valid_account = False

        # Check if the API response is successful
        if response.status_code == 200:
            # Parse account details from the response
            account_details = response.json()
            # Iterate through account details and check for a match
            for account in account_details:
                if (
                        account['accountType'] == account_type and
                        account['accountNumber'] == account_number and
                        account['password'] == password and
                        account['server'] == server_name
                ):
                    valid_account = True
                    break

        # If the account details are valid, save the new account
        if valid_account:
            # Create a new account instance
            account = Account(
                account_type=account_type,
                description_name=description_name,
                account_number=account_number,
                password=password,
                broker=broker_name,
                server=server_name
            )
            # Save the new account to the database
            account.save()

            # Add a success message
            messages.success(request, 'Account added successfully!')

            # Redirect to the accounts page after adding the account
            return redirect(reverse('account_view'))
        else:
            # Add an error message if the account is not valid
            messages.error(request, 'No matching account found. Please check your account details.')

    # Handle GET request: fetch brokers and servers from the API
    # Set a default value for brokers (an empty list)
    api_url = 'http://localhost:3000/api/brokers'
    response = requests.get(api_url)

    # Validate the response status code and fetch brokers if successful
    if response.status_code == 200:
        brokers = response.json()
        # Fetch servers for each broker
        for broker in brokers:
            broker_name = broker['name']
            server_url = f'http://localhost:3000/api/brokers/{broker_name}/servers'
            server_response = requests.get(server_url)

            # Validate server response status code
            if server_response.status_code == 200:
                broker['servers'] = server_response.json()

    # Render the template with brokers and servers data
    return render(request, 'Add Account.html', {
        'brokers': brokers,
        'username': logged_in_user
    })


# def Account(request):
#     logged_in_user = request.session.get('logged_in_user')
#
#     # Check if the user is logged in
#     if logged_in_user:
#         # Retrieve all accounts from the Account model
#         accounts = Account.objects.all()
#
#         # Render the 'Account.html' template with the accounts
#         return render(request, 'Account.html', {'accounts': accounts})
#     else:
#         # If the user is not logged in, redirect to the login page
#         return redirect('login')
#
#
#
# from django.contrib import messages
#
#
# from django.shortcuts import render, redirect
# from django.urls import reverse
# from django.http import HttpResponse
# from .models import Account
# import requests
#
# def Add_Account(request):
#     # Get logged-in user's name from the session
#     logged_in_user = request.session.get('logged_in_user')
#
#     # Redirect to login page if not logged in
#     if not logged_in_user:
#         return redirect('login')
#
#     # Handle POST request
#     if request.method == 'POST':
#         account_type = request.POST.get('accountType')
#         description_name = request.POST.get('descriptionName')
#         account_number = request.POST.get('accountNumber')
#         password = request.POST.get('password')
#         broker = request.POST.get('broker')
#         server = request.POST.get('server')
#
#         # Create and save the account
#         account = Account(
#             account_type=account_type,
#             description_name=description_name,
#             account_number=account_number,
#             password=password,
#             broker=broker,
#             server=server
#         )
#         account.save()
#
#         # Redirect to the accounts page after adding the account
#         return redirect(reverse('Account'))
#
#     # Handle GET request
#     # Fetch brokers and servers from the API
#     api_url = 'http://localhost:3000/api/brokers'
#     response = requests.get(api_url)
#     brokers = []
#
#     if response.status_code == 200:
#         brokers = response.json()
#
#         # Retrieve servers for each broker
#         for broker in brokers:
#             broker_name = broker['name']
#             server_url = f'http://localhost:3000/api/brokers/{broker_name}/servers'
#             server_response = requests.get(server_url)
#             if server_response.status_code == 200:
#                 broker['servers'] = server_response.json()
#
#     # Render the template with brokers and servers
#     return render(request, 'Add Account.html', {
#         'brokers': brokers,
#         'username': logged_in_user
#     })



def Trade_Copy(request):
    logged_in_user = request.session.get('logged_in_user')
    if logged_in_user:
        return render(request, 'Trade Copy.html', {'username': logged_in_user})
    else:
        return redirect('login')
def Equity_Monitors(request):
    logged_in_user = request.session.get('logged_in_user')
    if logged_in_user:
        return render(request, 'Equity Monitors.html', {'username': logged_in_user})
    else:
        return redirect('login')
def Email_Alerts(request):
    logged_in_user = request.session.get('logged_in_user')
    if logged_in_user:
        return render(request, 'Email Alerts.html', {'username': logged_in_user})
    else:
        return redirect('login')


from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .models import Account


def delete_account(request, account_id):
    # Get the account object using the account_id or return a 404 error if not found
    account = get_object_or_404(Account, id=account_id)

    # Delete the account object
    account.delete()

    # Redirect to the account listing page after deletion
    return redirect(reverse('account_view'))

