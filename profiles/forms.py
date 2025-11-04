from django import forms
from .models import UserProfile, PetProfile

class DateInput(forms.DateInput):
    input_type = "date"

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["avatar_image", "role", "phone", "birthdate", "location"]
        widgets = {
            "birthdate": DateInput(attrs={"class": "form-control"}),
            "role": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "location": forms.TextInput(attrs={"class": "form-control"}),
        }

class PetProfileForm(forms.ModelForm):
    class Meta:
        model = PetProfile
        fields = ["name", "avatar_image", "species", "sex", "birthdate", "color", "weight_kg"]
        widgets = {
            "birthdate": DateInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "species": forms.TextInput(attrs={"class": "form-control"}),
            "sex": forms.Select(attrs={"class": "form-control"}),
            "color": forms.TextInput(attrs={"class": "form-control"}),
            "weight_kg": forms.NumberInput(attrs={"step": "0.01", "class": "form-control"}),
        }
