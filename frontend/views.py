from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.exceptions import SuspiciousOperation

# VIEWS
from django.views import View


from app import models
from app import views
from frontend import forms



# Create your views here.
class TemplateBaseRoute:
	def index(self, request):
		return render(request, 'index.html')
	
	def tourism(self, request, id):
		return render(request, 'site.html')
	

class AccountSettings(View):
	__template_name = 'account_detail.html'
	
	def get(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('frontend:index')

		# Check user personalization
		categories = models.CategoryTourism.objects.all()
		personal_categories = list(models.UserPersonalization.objects.filter(user=request.user).order_by('category').values_list('category', flat=True).distinct('category'))

		# Account Details Form
		form = forms.EditUserForm(instance=request.user)

		return render(request, self.__template_name, 
		{
			'categories':categories,
			'personal_categories':personal_categories,
			'form':form
		})


	def post(self, request, *args, **kwargs):
		if not request.user.is_authenticated:
			return redirect('frontend:index')

		if(request.method == 'POST'):
			user = forms.EditUserForm(request.POST, instance=request.user)
			if user.is_valid():
				user.save()
				messages.success(request, 'User successfully changed')
			else:
				messages.error(request, 'User successfully changed')

		return redirect('frontend:account_settings')


class User:
	__template_name = 'accounts/login_register.html'

	def register(self, request):
		if request.user.is_authenticated:
			return redirect('frontend:index')
		
		if(request.method=='POST'):
			email, password, age = request.POST['email'], request.POST['password'], request.POST['age']

			if int(request.POST['age']) < 18:
				messages.error(request, 'Umur pendaftar minimal 18 tahun')
				return redirect('frontend:account_login')

			try:
				user = models.AccountCustom.objects.get(email=email)
			except:
				try:
					user = models.AccountCustom.objects.create_user(email=email,password=password,age=age)
					if(user):
						user.save()
				except:
					raise SuspiciousOperation
				else:
					user = authenticate(request, email=email, password=password)

					if(user is not None):
						login(request, user)
					
					return redirect('frontend:account_early_configuration')

			else:
				messages.add_message(request, messages.ERROR, 'Duplikasi akun ditemukan. Gunakan akun yang berbeda')
				return redirect('frontend:account_login')
	
	def login(self, request):
		if request.user.is_authenticated:
			return redirect('frontend:index')

		if(request.method=='POST'):
			email, password = request.POST['email'], request.POST['password']
			user = authenticate(request, email=email, password=password)

			if(user is not None):
				login(request, user)


			else:
				messages.error(request, 'Account or password invalid')
				return redirect('frontend:account_login')


			if('next' in request.POST):
				return redirect(request.POST['next'])

			if user.is_staff:
				return redirect('admin:index')

			return redirect('frontend:index')

		loginForm = forms.Authenticate()
		registrationForm = forms.Registration()	
		return render(
			request, 
			self.__template_name, 
			{
				'loginForm':loginForm,
				'registrationForm':registrationForm
			}
		)
	
	def signout(self, request):
		if not request.user.is_authenticated:
			return redirect('frontend:index')

		logout(request)
		return redirect('frontend:index')
	
	def history_receipt(self, request, id):
		content = models.Reservation.objects.get(reservation_id=id)

		return render(
			request, 
			"accounts/history_receipt.html",
			{
				'content':content
			}
		)

class UserPersonalization:
	def early_personalization(self, request):
		if request.method == 'GET':
			tourism = models.TourismPlace.objects.all()[:30]
			return render(request, 'accounts/early_configuration.html',{'contents':tourism})
		else:
			id_tourism = [i for i in request.POST.getlist('tourism_personalization')]

			categories = models.TourismPlace.objects.filter(pk__in=id_tourism).values('category__category_name')

			for i in [list(i.values())[0] for i in categories]:
				category = models.CategoryTourism.objects.get(category_name=i)
				personal_category = models.UserPersonalization(user=request.user, category=category)
				personal_category.save()

			data = {
				'place':id_tourism,
				'user':[request.user.id]
			}

			views.MODEL_RECC.update_model(data, categories, new_data=1)

		return redirect('frontend:index')
		
	def personalization(self, request):
		if not request.user.is_authenticated:
			return redirect('frontend:index')

		categories = [i for i in request.POST.getlist('categories')]

		# Change categories
		models.UserPersonalization.objects.filter(user=request.user).delete()

		for i in categories:
			category = models.CategoryTourism.objects.get(category_id=i)
			personal_category = models.UserPersonalization(user=request.user, category=category)
			personal_category.save()
				

		return redirect('frontend:account_settings')


	




