from django.apps import AppConfig
from django.db.models.signals import post_migrate

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from django.contrib.auth.models import Group
        
        def create_groups(sender, **kwargs):
            Group.objects.get_or_create(name='Clients')
            Group.objects.get_or_create(name='Doctors')
        
        post_migrate.connect(create_groups, sender=self)