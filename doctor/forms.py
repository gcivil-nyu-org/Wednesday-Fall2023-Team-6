from django import forms
from .models import Doctor


class DoctorFilterForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "doctor-name-input",
                "placeholder": "Search for doctor's name",
            }
        ),
        required=False,
    )
    primary_speciality = forms.ModelChoiceField(
        queryset=Doctor.objects.values_list("primary_speciality", flat=True).distinct(),
        widget=forms.Select(attrs={"class": "custom-select"}),
        required=False,
    )
    address = forms.ModelChoiceField(
        queryset=Doctor.objects.values_list("address", flat=True).distinct(),
        widget=forms.Select(attrs={"class": "custom-select"}),
        required=False,
    )
    borough = forms.ModelChoiceField(
        queryset=Doctor.objects.values_list("borough", flat=True).distinct(),
        widget=forms.Select(attrs={"class": "custom-select"}),
        required=False,
    )
    zip = forms.ModelChoiceField(
        queryset=Doctor.objects.values_list("zip", flat=True).distinct(),
        widget=forms.Select(attrs={"class": "custom-select"}),
        required=False,
    )

    class Meta:
        model = Doctor
        fields = ("name", "primary_speciality", "address", "borough", "zip")
