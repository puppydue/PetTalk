# profiles/forms.py
from django import forms
from .models import UserProfile, PetProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["avatar_image", "phone", "birthdate", "location"]
        widgets = {
            "birthdate": forms.DateInput(attrs={"type": "date"}),
        }

class PetProfileForm(forms.ModelForm):
    class Meta:
        model = PetProfile
        fields = ["name", "avatar_image", "species", "sex", "birthdate", "color", "weight_kg"]
        widgets = {
            "birthdate": forms.DateInput(attrs={"type": "date"}),
            "sex": forms.Select(),
            "weight_kg": forms.NumberInput(attrs={"step": "0.1"}),
        }
