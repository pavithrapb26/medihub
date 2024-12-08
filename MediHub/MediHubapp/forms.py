from django import forms
from .models import Prescription

class PrescriptionUploadForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['prescription_file']
        widgets = {
            'prescription_file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
