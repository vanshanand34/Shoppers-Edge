from django import forms

class shoppingform(forms.Form):
    product = forms.CharField(label="Search Product",)