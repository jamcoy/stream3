from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail
from settings.dev import EMAIL_TO, DEFAULT_FROM_EMAIL
from django.contrib import messages


def index(request):
    return render(request, 'complementary_pages/index.html')


def about(request):
    return render(request, 'complementary_pages/about.html')


def terms(request):
    return render(request, 'complementary_pages/terms.html')


def contact(request):

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            user_subject = form.cleaned_data['user_subject']
            contact_name = form.cleaned_data['contact_name']
            from_email = form.cleaned_data['from_email']
            message = form.cleaned_data['message']

            subject = "EasyFuelTracker contact from " + contact_name

            message = "Name: " + contact_name + "\n" \
                      + "Subject: " + user_subject + "\n" \
                      + "User's email: " + from_email + "\n" + "\n" \
                      + message

            send_mail(subject, message, DEFAULT_FROM_EMAIL, [EMAIL_TO], fail_silently=False)

            messages.success(request, "Your message has been sent. We'll be in touch soon.")

            return redirect('contact')

    else:
        form = ContactForm()

        return render(request, 'complementary_pages/contact.html', {'form': form})
