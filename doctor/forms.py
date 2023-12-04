from django import forms

from user.models import Choices
from .models import Doctor


class DoctorFilterForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "doctor-name-input",
                "placeholder": "Search doctor name",
            }
        ),
        required=False,
    )
    
    ratings = forms.ChoiceField(
        choices=[
            ("0", "More than 0 (0-5 ratings)"),
            ("1", "More than 1 (2-5 ratings)"),
            ("2", "More than 2 (3-5 ratings)"),
            ("3", "More than 3 (4-5 ratings)"),
            ("4", "More than 4 (5 ratings)"),
        ],
        widget=forms.Select(attrs={"class": "custom-select"}),
        required=False,
    )
    

    primary_speciality = forms.ChoiceField(
        # queryset=Doctor.objects.values_list("primary_speciality", flat=True).distinct(),
        widget=forms.Select(attrs={"class": "custom-select"}),
        required=False,
    )
    address = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "custom-select"}),
        required=False,
    )
    borough = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "custom-select"}),
        required=False,
    )
    zip = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "custom-select"}),
        required=False,
    )

    class Meta:
        model = Doctor
        fields = ("name", "primary_speciality", "address", "borough", "zip")

    def __init__(self, *args, **kwargs):
        super(DoctorFilterForm, self).__init__(*args, **kwargs)

        """
        Get filter values from request parameters
        to keep the searching value of users after redirecting the page
        """
        initial_values = {
            "name": self.data.get("name", ""),
            "primary_speciality": self.data.get("primary_speciality", "All"),
            "address": self.data.get("address", "All"),
            "borough": self.data.get("borough", "All"),
            "zip": self.data.get("zip", "All"),
        }

        """
        add "All" options for filter as the initial value
        """
        all_option = [("All", "All")]

        # Add an "all" option to the fields
        self.fields["name"].initial = initial_values["name"]

        specialities = list(
            Doctor.objects.values_list("primary_speciality", flat=True).distinct()
        )
        all_specialities = all_option + [
            (speciality, speciality) for speciality in specialities
        ]
        self.fields["primary_speciality"].choices = all_specialities
        self.fields["primary_speciality"].initial = initial_values["primary_speciality"]

        addresses = list(Doctor.objects.values_list("address", flat=True).distinct())
        all_address = all_option + [(address, address) for address in addresses]
        self.fields["address"].choices = all_address
        self.fields["address"].initial = initial_values["address"]

        all_borough = all_option + [(bor[0], bor[1]) for bor in Choices.boroughs]
        self.fields["borough"].choices = all_borough
        self.fields["borough"].initial = initial_values["borough"]

        zip_codes = list(Doctor.objects.values_list("zip", flat=True).distinct())
        all_zip = all_option + [(zip, zip) for zip in zip_codes]
        self.fields["zip"].choices = all_zip
        self.fields["zip"].initial = initial_values["zip"]