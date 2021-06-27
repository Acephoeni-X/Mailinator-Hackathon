from email import message
from django import forms

class sendMail(forms.Form):
    to_email = forms.CharField(label='To', widget=forms.EmailInput(attrs={'placeholder':'Email'}))
    subject = forms.CharField(label='Subject', widget=forms.TextInput(attrs={'placeholder':'Subject'}))
    message = forms.CharField(label='Enter your Message', widget=forms.Textarea)
    time = forms.CharField(label='Enter time of message', widget=forms.TextInput(attrs={'placeholder':'Enter time'}))