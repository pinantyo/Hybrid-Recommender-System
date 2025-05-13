from django import forms
from app import models


class Authenticate(forms.ModelForm):
	email = forms.EmailField(
		widget=forms.EmailInput(attrs={'class':'form-control'}),
		label='email',
		max_length=254, 
		required=True)
	password = forms.CharField(
		widget=forms.PasswordInput(attrs={'class':'form-control'}), 
		label='password', 
		required=True, 
		max_length=100
	)

	class Meta:
		model = models.AccountCustom
		fields = ('email','password')

class Registration(forms.ModelForm):
	email = forms.EmailField(
		widget=forms.EmailInput(attrs={'class':'form-control'}),
		label='email',
		max_length=254, 
		required=True
	)
	password = forms.CharField(
		widget=forms.PasswordInput(attrs={'class':'form-control'}), 
		label='password', 
		required=True, 
		max_length=100
	)
	age = forms.IntegerField(
		widget=forms.NumberInput(attrs={'class':'form-control'}),
		min_value=18,
		max_value=90
	)


	class Meta:
		model = models.AccountCustom
		fields = ('email','password','age')


class EditUserForm(forms.ModelForm):
    email = forms.EmailField(
		widget=forms.EmailInput(attrs={'class':'form-control'}),
		label='email',
		max_length=254, 
		required=True
	)

    full_name = forms.CharField(
		widget=forms.TextInput(attrs={'class':'form-control'}),
		label='full_name',
		max_length=300, 
		required=False
	)
    age = forms.IntegerField(
		widget=forms.NumberInput(attrs={'class':'form-control'}),
		label='age', 
		required=False,
		min_value=18,
		max_value=90
	)
    location = forms.CharField(
		widget=forms.TextInput(attrs={'class':'form-control'}),
		label='location',
		max_length=1000, 
		required=False
	)

    password = forms.CharField(
		widget=forms.PasswordInput(attrs={'class':'form-control'}),
		label='password', 
		required=True, 
		max_length=500
	)

    class Meta:
        model = models.AccountCustom
        fields = ('email','full_name','age','location', 'password')

    """
        Pengaturan Password
    """
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class ReservationForm(forms.ModelForm):
    user_id = forms.IntegerField()
    place_id = forms.IntegerField()
    due_date = forms.DateTimeField(required=True, widget=forms.TextInput(attrs={"type":"datetime-local"}))
    
    class Meta:
        model = models.Reservation
        fields = ('user','place','due_date')