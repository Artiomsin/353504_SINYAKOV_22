from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import User, Group
from .models import (
    GroupProxy, 
    Client, Doctor, News, Employee, Vacancy,
    GlossaryTerm, Cabinet, Specialization,
    Service, Appointment, PromoCode, Review,
    UserProfile,
)

class ClientAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'birth_date')
    search_fields = ('user__username', 'phone')

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    filter_horizontal = ('specializations', 'services') 
    list_display = ('full_name', 'cabinet', 'experience')
    search_fields = ('full_name', 'license_number')
    
    fieldsets = (
        (None, {
            'fields': ('user', 'full_name', 'photo', 'phone', 'email', 'experience')
        }),
        ('Профессиональная информация', {
            'fields': ('cabinet', 'specializations', 'services', 'license_number')
        }),
        ('Даты', {
            'fields': ('start_date',),
            'classes': ('collapse',)
        }),
    )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change:  # только при создании нового доктора
            clients_group = Group.objects.get(name='Clients')
            obj.user.groups.remove(clients_group)

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'publish_date')

admin.site.register([Employee, Vacancy])

@admin.register(GlossaryTerm)
class GlossaryAdmin(admin.ModelAdmin):
    list_display = ('term', 'date_added')
    search_fields = ('term', 'definition')

admin.site.register(Client, ClientAdmin)
admin.site.register(Cabinet)
admin.site.register(Specialization)
admin.site.register(Service)
admin.site.register(Appointment)

@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount', 'valid_until', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('code',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'date')
    list_filter = ('rating', 'date')

@admin.register(GroupProxy)
class CustomGroupAdmin(GroupAdmin):
    list_display = ('name', 'get_users_count')
    
    def get_users_count(self, obj):
        return obj.user_set.count()
    get_users_count.short_description = 'Количество пользователей'

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'get_groups', 'is_staff')
    
    def get_groups(self, obj):
        return ", ".join([g.name for g in obj.groups.all()])
    get_groups.short_description = 'Группы'

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'timezone')