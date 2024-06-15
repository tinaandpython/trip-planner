from django import forms


class ItineraryGeneratorForm(forms.Form):
    destination = forms.CharField(max_length=255, label='Destination')
    days = forms.IntegerField(min_value=1, label='Number of days')



