from django.shortcuts import redirect
from django.contrib.auth.mixins import UserPassesTestMixin

class DoctorRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Doctors').exists() and hasattr(self.request.user, 'doctor')
    
    def handle_no_permission(self):
        return redirect('home')

class ClientRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.groups.filter(name='Clients').exists() and hasattr(self.request.user, 'client')
    
    def handle_no_permission(self):
        return redirect('home')