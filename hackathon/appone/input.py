from email import message
from django import forms

class sendMail(forms.Form):

    to_email = forms.CharField(label='To', widget=forms.EmailInput(attrs={'placeholder':'Email'}))
    subject = forms.CharField(label='Subject', widget=forms.TextInput(attrs={'placeholder':'Subject'}))
    message = forms.CharField(label='Enter your Message', widget=forms.Textarea)
    
    hr = forms.CharField(label='Enter time of message', required=False, widget=forms.TextInput(attrs={'placeholder':'Enter Hour'}))
    mint = forms.CharField(label='Enter time of message', required=False, widget=forms.TextInput(attrs={'placeholder':'Enter Min'}))
    sec = forms.CharField(label='Enter time of message', required=False, widget=forms.TextInput(attrs={'placeholder':'Enter Sec'}))
