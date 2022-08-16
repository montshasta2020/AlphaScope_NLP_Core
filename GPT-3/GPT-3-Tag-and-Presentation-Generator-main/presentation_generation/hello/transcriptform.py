from django import forms

class TranscriptForm(forms.Form):
    transcript_field = forms.CharField(label="Enter video transcript here", max_length=2000)
