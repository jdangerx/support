from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from support.models import SupplementalMaterial

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    def save(self, commit=True):
        user = super(UserCreationForm, self).save()
        user.email = self.cleaned_data.get('email')
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class SupplementalMaterialForm(ModelForm):
    class Meta:
        model = SupplementalMaterial
        fields = ['name','material_file']

