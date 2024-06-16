from django import forms

class ItineraryGeneratorForm(forms.Form):
    destination = forms.CharField(
        max_length=255,
        label='Destination',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    days = forms.IntegerField(
        min_value=1,
        label='Number of days',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )



