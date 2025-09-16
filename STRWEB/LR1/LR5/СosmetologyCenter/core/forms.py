from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from .models import Client, Review, Appointment
from django.contrib.auth.forms import PasswordChangeForm
import pytz

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Ваш отзыв...'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select'
            })
        }
        labels = {
            'rating': 'Оценка',
            'text': 'Текст отзыва'
        }

class ClientSignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, 
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        label="Телефон",
        help_text="Формат: +375 (29) XXX-XX-XX",
        validators=[Client._meta.get_field('phone').validators[0]]
    )
    birth_date = forms.DateField(
        label="Дата рождения",
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    address = forms.CharField(label="Адрес", widget=forms.Textarea)

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            Client.objects.get_or_create(
                user=user,
                defaults={
                    'phone': self.cleaned_data['phone'],
                    'birth_date': self.cleaned_data['birth_date'],
                    'address': self.cleaned_data['address']
                }
            )
            user.groups.add(Group.objects.get(name='Clients'))
        return user
    
class ClientProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    
    class Meta:
        model = Client
        fields = ['phone', 'birth_date', 'address']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = self.instance.user.username
        self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        user = self.instance.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.save()
        return super().save(commit)

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Старый пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label="Подтверждение нового пароля",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['date_time']
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CompleteAppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['doctor_notes']
        widgets = {
            'doctor_notes': forms.Textarea(attrs={'rows': 4})
        }

class TimezoneForm(forms.Form):
    timezone = forms.ChoiceField(
        choices=[(tz, tz) for tz in pytz.all_timezones],
        label="Выберите вашу временную зону"
    )