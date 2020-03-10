from django import forms


class AnalyzeUrlForm(forms.Form):
    url = forms.URLField(label='Enter a url')