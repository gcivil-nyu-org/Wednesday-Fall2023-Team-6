from django import forms

from user.models import Choices
from .models import Hospital


class HospitalFilterForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "hospital-name-input",
                "placeholder": "Search hospital name",
                "name": "search",
            }
        ),
        required=False,
    )
    facility_type = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "custom-select"}),
        required=False,
    )
    location = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "custom-select"}),
        required=False,
    )
    borough = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "custom-select"}),
        required=False,
    )
    postal_code = forms.ChoiceField(
        widget=forms.Select(attrs={"class": "custom-select"}),
        required=False,
    )

    class Meta:
        model = Hospital
        fields = ("name", "facility_type", "location", "borough", "postal_code")

    def __init__(self, *args, **kwargs):
        super(HospitalFilterForm, self).__init__(*args, **kwargs)

        """
        Get filter values from request parameters
        to keep the searching value of users after redirecting the page
        """
        initial_values = {
            "name": self.data.get("name", ""),
            "facility_type": self.data.get("facility_type", "All"),
            "location": self.data.get("location", "All"),
            "borough": self.data.get("borough", "All"),
            "postal_code": self.data.get("postal_code", "All"),
        }

        """
        add "All" options for filter as the initial value
        """
        all_option = [("All", "All")]

        # Add an "all" option to the fields
        self.fields["name"].initial = initial_values["name"]

        types = list(
            Hospital.objects.values_list("facility_type", flat=True).distinct()
        )
        all_facility_types = all_option + [(type, type) for type in types]
        self.fields["facility_type"].choices = all_facility_types
        self.fields["facility_type"].initial = initial_values["facility_type"]

        locations = list(Hospital.objects.values_list("location", flat=True).distinct())
        all_locations = all_option + [(location, location) for location in locations]
        self.fields["location"].choices = all_locations
        self.fields["location"].initial = initial_values["location"]

        all_borough = all_option + [(bor[0], bor[1]) for bor in Choices.boroughs]
        self.fields["borough"].choices = all_borough
        self.fields["borough"].initial = initial_values["borough"]

        postal_codes = list(
            Hospital.objects.values_list("postal_code", flat=True).distinct()
        )
        all_postal_codes = all_option + [
            (postal_code, postal_code) for postal_code in postal_codes
        ]
        self.fields["postal_code"].choices = all_postal_codes
        self.fields["postal_code"].initial = initial_values["postal_code"]
