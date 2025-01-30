from django import forms

class ReserveSlotForm(forms.Form):
    name = forms.CharField(max_length=100)
    pin = forms.IntegerField()
