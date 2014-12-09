from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from support.models import SupplementalMaterial, UserProfile

class SignUpForm(UserCreationForm):
    email = forms.EmailField()
    description = forms.CharField(widget=forms.Textarea)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save()
        user.email = self.cleaned_data.get('email')
        user.set_password(self.cleaned_data["password1"])
        userprofile = UserProfile.objects.create(user=user, intro_text=self.cleaned_data.get('description'))
        if commit:
            user.save()
            userprofile.save()
        return user

class SupplementalMaterialForm(ModelForm):
    class Meta:
        model = SupplementalMaterial
        fields = ['name','material_file']

