from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Role

class CustomUserForm(forms.ModelForm):
    roles = forms.ModelChoiceField(
        queryset=Role.objects.all(),
        widget=forms.Select,
        required=True,
        label="Selecciona un rol",
    )
    new_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label="Nueva Contraseña",
        help_text="Déjalo en blanco si no deseas cambiar la contraseña."
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput,
        required=False,
        label="Confirmar Nueva Contraseña"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'roles', 'is_active', 'new_password', 'confirm_password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Ya existe una cuenta con este correo.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password or confirm_password:
            if new_password != confirm_password:
                self.add_error("confirm_password", "Las contraseñas no coinciden.")

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get("new_password")

        if new_password:
            user.password = make_password(new_password)

        if commit:
            user.save()
            user.roles.set(self.cleaned_data['roles'])
        return user
