from django import forms

CHART_CHOICES = (
    ('barchart', 'Bar chart'),
    ('piechart', 'Pie chart'),
    ('linechart', 'Line chart')
)

RESULT_CHOICES = (
    ('transaction', 'Transaction'),
    ('sales_date', 'Sales date'),
)
class SalesSearchForm(forms.Form):
    date_from = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    date_to = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    chart_type = forms.ChoiceField(choices=CHART_CHOICES)
    results_by = forms.ChoiceField(choices=RESULT_CHOICES)