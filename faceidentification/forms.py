from django import forms

class AddonForm(forms.ModelForm):
    addon_name = forms.CharField(max_length=100, required=True)
    image = forms.ImageField(required=False)