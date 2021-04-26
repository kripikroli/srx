from django import forms

CHART_CHOICES = (
    ('#1', 'Bar chart'),
    ('#2', 'Pie chart'),
    ('#3', 'Line chart')
)
class SalesSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    chart_type = forms.ChoiceField(choices=CHART_CHOICES)