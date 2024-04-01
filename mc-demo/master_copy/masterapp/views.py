from email.message import EmailMessage

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




