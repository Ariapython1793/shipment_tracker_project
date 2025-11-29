# tracking/forms.py
from django import forms
from .models import Container, ContainerStatus

class ContainerForm(forms.ModelForm):
    class Meta:
        model = Container
        fields = ['container_number', 'origin', 'destination', 'status', 'depart_time', 'distance_km', 'avg_speed_kmh']
        widgets = {
            'depart_time': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

class ContainerSearchForm(forms.Form):
    query = forms.CharField(required=False, label='Search container/origin/destination')
    status = forms.ChoiceField(choices=[('', 'All')] + list(ContainerStatus.choices), required=False)
    destination = forms.CharField(required=False)
    origin = forms.CharField(required=False)
