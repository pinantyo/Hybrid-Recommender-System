from django.contrib import admin
from app import models, forms

from django.contrib.auth.admin import UserAdmin

# Register your models here.



# Inline
class PersonalizationInLine(admin.TabularInline):
    model = models.UserPersonalization

class PackageSitesInLine(admin.TabularInline):
    model = models.PackageSites
    


# Class Admin
class UserAdmin(UserAdmin):
    form = forms.UserChangeForm
    add_form = forms.UserCreationForm

    list_display = ('email', 'full_name', 'is_admin','is_staff','is_superuser','created')
    list_filter = ('is_admin','is_staff','is_superuser')
    fieldsets = (
        ('Account Information', {'fields': ('email', 'password')}),
        ('Personal Information', {'fields': ('full_name','location','phone_number')}),
        ('Permissions', {'fields': ('is_admin', 'is_active','is_staff','is_superuser')}),
    )

    # overrides
    add_fieldsets = (
        ('Account Information', {
            'classes': ('wide',),
            'fields': ('email','password', 'password2')}
        ),('Personal Information', {
            'classes': ('wide',),
            'fields': ('full_name','age','location')}
        )
    )
    search_fields = ('email','full_name','location')
    ordering = ('created',)
    inlines = [PersonalizationInLine]
    list_per_page = 10
    filter_horizontal = ()
    
# Class Tourism
class TourismPlaceAdmin(admin.ModelAdmin):
    form = forms.TourismChangeForm
    add_form = forms.TourismCreationForm
    list_display = ('category','place_name','city','price','rating')
    list_filter = ('category','city',)

	# Form
    fieldsets = (
        ('General', {'fields': ('place_name', 'description','city','price','time_minutes','img')}),
        ('Personalized', {'fields': ('category',)}),
		('Location', {'fields': ('lat','long')}),
    )
    # overrides
    add_fieldsets = (
        ('General', {
            'classes': ('wide',),
            'fields': ('place_name', 'description','city','price','time_minutes','img')}
        ),('Personalized', {
            'classes': ('wide',),
            'fields': ('category',)}
        ),('Location', {
			'classes': ('wide',),
			'fields': ('lat','long')}
		)
    )
    search_fields = ('category__category_name','place_name','city', 'description')
    ordering = ('rating',)
    list_per_page = 10

class ReservationAdmin(admin.ModelAdmin):
    list_select_related = ('user', 'place')
    # readonly_fields = ('email','full_name','location','phone_number')
    list_display=('user','place','place_ratings','comments','status','book_date','time')
    list_filter=('status',)
    search_fields=('place__place_name','comments','status')
    ordering=('time',)
    list_per_page = 10


class PackageTourismAdmin(admin.ModelAdmin):
    list_display = ('package_name','description')
    search_fields = ('package_name','description')
    inlines = [PackageSitesInLine]
    list_per_page = 10

class LogsAdmin(admin.ModelAdmin):
    list_display = ('user','content_type','action_flag','action_time')
    readonly_fields = ('action_time','user','content_type','object_id','object_repr','action_flag','change_message')
    list_filter = ('action_flag',)
    ordering=('action_time',)
    list_per_page = 10


admin.site.register(models.AccountCustom, UserAdmin)
admin.site.register(models.TourismPlace, TourismPlaceAdmin)
admin.site.register(models.CategoryTourism)
admin.site.register(models.PackageTourism, PackageTourismAdmin)
admin.site.register(models.Reservation, ReservationAdmin)
admin.site.register(admin.models.LogEntry, LogsAdmin)



