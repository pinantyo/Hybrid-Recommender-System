from django.contrib.auth import views as authView
from django.urls import path, reverse_lazy

from frontend import views



app_name = 'frontend'

urlpatterns = [
	path('', views.TemplateBaseRoute().index, name='index'),

	# Accounts
	path('account/', views.AccountSettings.as_view(), name='account_settings'),
    path('account/login/', views.User().login, name='account_login'),
    path('account/register/', views.User().register, name='account_register'),
    path('account/logout/', views.User().signout, name='account_logout'),
    path('account/configuration/', views.UserPersonalization().early_personalization, name='account_early_configuration'),
    path('account/personalization/', views.UserPersonalization().personalization, name='account_personalization'),
    path('account/reservation-receipt/<int:id>', views.User().history_receipt, name='account_reservation_receipt'),

	# Tourism
	path('tourism-place/<int:id>', views.TemplateBaseRoute().tourism, name='tourism_site'),

	# Reset Password
	path('password_reset/', authView.PasswordResetView.as_view(template_name='accounts/password_configuration/password_reset_form.html',
        email_template_name='accounts/password_configuration/password_reset_email_template.html',
        success_url = reverse_lazy('frontend:password_reset_done')),
        name='password_reset'),
    path('reset/<uidb64>/<token>/', authView.PasswordResetConfirmView.as_view(template_name="accounts/password_configuration/password_reset_confirm.html",
        success_url = reverse_lazy('frontend:password_reset_complete')),
        name='password_reset_confirm'),
    path('reset/success/', authView.PasswordResetCompleteView.as_view(template_name='accounts/password_configuration/password_reset_complete.html'), 
        name='password_reset_complete'),
    path('password_reset/success/', authView.PasswordResetDoneView.as_view(template_name='accounts/password_configuration/password_reset_done.html'), 
        name='password_reset_done'),

]