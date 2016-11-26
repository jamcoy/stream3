from django import forms


class PlateForm(forms.Form):
    your_reg = forms.CharField(label='Registration', max_length=20)
