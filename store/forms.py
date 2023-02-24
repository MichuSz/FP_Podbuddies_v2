from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT = (
    ('S','Stripe'),
    ('P','PayPal')
)


class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'White Eagle Refugee Camp'}))
    apartment_address = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Apartment or bunker'}))
    country = CountryField(blank_label='(select country)').formfield(widget=CountrySelectWidget(attrs={'class':'custom-select d-block w-100'}))
    zip = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}))

    payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT)