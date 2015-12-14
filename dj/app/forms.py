from django import forms


class AddForm(forms.Form):
    user = forms.IntegerField(required=True)
    url = forms.CharField(required=True)