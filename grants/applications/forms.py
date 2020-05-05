from django import forms

from grants.applications.models import ApplicationProcess, ApplicationNotes


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = ApplicationProcess
        fields = ['full_name', 'email', 'proposal', 'requested_amount']

