from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "message"]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Your Name",
                "class": "contact-input"
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Your Email",
                "class": "contact-input"
            }),
            "message": forms.Textarea(attrs={
                "placeholder": "Your Message",
                "class": "contact-input",
                "rows": 6
            }),
        }

from .models import Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "phone", "address"]

        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Full Name",
                "class": "checkout-input"
            }),
            "phone": forms.TextInput(attrs={
                "placeholder": "Phone Number",
                "class": "checkout-input"
            }),
            "address": forms.Textarea(attrs={
                "placeholder": "Delivery Address",
                "class": "checkout-input",
                "rows": 4
            }),
        }
