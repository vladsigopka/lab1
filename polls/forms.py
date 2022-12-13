from django import forms
from django.core.validators import EmailValidator
from django.core.validators import RegexValidator, FileExtensionValidator
from .models import User, Question, Choice


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput,
                               validators=[RegexValidator(r'[a-zA-Z\-]', 'В логине доступны только латинские символы')],
                               required=True)

    full_name = forms.CharField(label='ФИО', widget=forms.TextInput,
                                validators=[RegexValidator(r'[а-яА-ЯёЁ\-\s]',
                                                           'В ФИО доступна только кириллица')],
                                required=True)

    password = forms.CharField(label='пароль', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='повторите пароль', widget=forms.PasswordInput, required=True)
    email = forms.EmailField(label='Email', widget=forms.EmailInput, required=True,
                             validators=[EmailValidator('Email не верен')])
    avatar = forms.ImageField(label="выберите аватар",
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp'])],
                              required=False)
    checkbox = forms.CharField(label='соглашение на обработку данных', widget=forms.CheckboxInput,
                               required=False)

    class Meta:
        model = User
        fields = ['avatar', 'full_name', 'username', 'email', 'password', 'password2']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password2']

    def clean_checkbox(self):
        cd = self.cleaned_data
        if cd['checkbox'] == False:
            raise forms.ValidationError('Подтвердите обработку персональных данных')
        return cd['checkbox']

    def clean_avatar(self):
        cd = self.cleaned_data
        if not cd['avatar']:
            cd['avatar'] = 'images/profile/grey_avatar.png'
        return cd['avatar']


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(label='Username', widget=forms.TextInput,
                               validators=[RegexValidator(r'[a-zA-Z\-]', 'В логине доступны только латинские символы')],
                               required=True)

    full_name = forms.CharField(label='ФИО', widget=forms.TextInput,
                                validators=[RegexValidator(r'[а-яА-ЯёЁ\-\s]',
                                                           'В ФИО доступна только кириллица, пробелы и дефис')],
                                required=True)
    email = forms.EmailField(label='Email', widget=forms.EmailInput, required=True,
                             validators=[EmailValidator('Email не верен')])
    avatar = forms.ImageField(label="Pic an avatar",
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'bmp'])],
                              required=False)

    def clean_avatar(self):
        cd = self.cleaned_data
        if not cd['avatar']:
            cd['avatar'] = '/images/profile/grey_avatar.png'
        return cd['avatar']

    class Meta:
        model = User
        fields = ['avatar', 'full_name', 'username', 'email']



