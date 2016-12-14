from django import forms


class ContactForm(forms.Form):
    user_subject = forms.CharField(label="Subject", required=True, max_length=50)
    contact_name = forms.CharField(label="Your name", required=True, max_length=50)
    from_email = forms.EmailField(label="Email", required=True)
    message = forms.CharField(required=True, widget=forms.Textarea)

