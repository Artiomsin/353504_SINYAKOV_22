from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView, CreateView, DeleteView, UpdateView
from .models import News, GlossaryTerm, Employee, Vacancy, Review, PromoCode, Doctor, Service, Purchase, Client, User
from .forms import ReviewForm, ClientProfileForm, AppointmentForm, CompleteAppointmentForm, ReviewForm, TimezoneForm
from django.urls import reverse_lazy
from .filters import ServiceFilter
from django.utils import timezone
import calendar
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse
from .utils import get_currency_rates
from .forms import ClientSignUpForm, ReviewForm
from .permissions import DoctorRequiredMixin, ClientRequiredMixin
from .models import Appointment
from django.shortcuts import redirect
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from .models import Service, Doctor, Appointment 
from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.db.models import Count, Sum, Avg
from django.db.models import Q
import logging
from io import BytesIO
import base64
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  
import numpy as np
from django.db.models import Case, When, F, FloatField

logger = logging.getLogger(__name__)

class HomeView(ListView):
    template_name = 'core/home.html'
    context_object_name = 'latest_news'
    
    def get_queryset(self):
        logger.debug("Получение последних новостей для главной страницы")
        return News.objects.order_by('-publish_date')[:3]
    
    def get_context_data(self, **kwargs):
        logger.info("Начало формирования контекста для главной страницы")
        context = super().get_context_data(**kwargs)

        context ['latest_news'] = News.objects.order_by('-publish_date')[:3]

        context['glossary_terms'] = GlossaryTerm.objects.all()[:5]
        
        context['reviews'] = Review.objects.all().order_by('-date')[:10]

        context['review_form'] = ReviewForm()

        try:
            logger.debug("Запрос курсов валют")
            currency_data = get_currency_rates()
            if 'error' in currency_data:
                logger.error(f"Ошибка при получении курсов валют: {currency_data['error']}")
            else:
                logger.debug("Данные о курсах валют успешно получены")
            context['currency'] = currency_data if 'error' not in currency_data else None
            context['currency_error'] = currency_data.get('error', None)
            
        except Exception as e:
            logger.exception("Ошибка при обработке внешних API")
        
        cal = calendar.TextCalendar()
        today = timezone.now()
        context['calendar'] = cal.formatmonth(
            theyear=today.year, 
            themonth=today.month
        )

        logger.info("Контекст для главной страницы успешно сформирован")
        return context
    
    def post(self, request, *args, **kwargs):
        form = ReviewForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Ваш отзыв успешно опубликован!')
        return redirect('home')
    
class ServiceListView(ListView):
    model = Service
    paginate_by = 10
    template_name = 'core/services.html'
    context_object_name = 'services'
    filterset_class = ServiceFilter
    
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs.distinct()


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.filterset
        return context
    
class AboutView(TemplateView):
    template_name = 'core/about.html'

class DoctorListView(ListView):
    model = Doctor
    template_name = 'core/doctors.html'
    context_object_name = 'doctors'
    paginate_by = 20
    def get_queryset(self):
        return Doctor.objects.all().select_related('cabinet').prefetch_related('specializations')
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['employees'] = Employee.objects.all()  
class DoctorDetailView(DetailView):
    model = Doctor
    template_name = 'core/doctor_detail.html'
    context_object_name = 'doctor'

class NewsListView(ListView):
    model = News
    template_name = 'core/news_list.html'
    context_object_name = 'news_list'
    ordering = ['-publish_date']
    paginate_by = 6

class NewsDetailView(DetailView):
    model = News
    template_name = 'core/news_detail.html'
    context_object_name = 'news'

class GlossaryListView(ListView):
    model = GlossaryTerm
    template_name = 'core/glossary.html'

class ContactsView(ListView):
    model = Employee
    template_name = 'core/contacts.html'

class PrivacyPolicyView(TemplateView):
    template_name = 'core/privacy_policy.html'

class VacancyListView(ListView):
    model = Vacancy
    template_name = 'core/vacancy_list.html'
    context_object_name = 'vacancies'
    ordering = ['-date_posted']
    paginate_by = 10

class ReviewCreateView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'core/add_review.html'
    success_url = reverse_lazy('reviews')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PromoCodeListView(ListView):
    model = PromoCode
    template_name = 'core/promocodes.html'
    context_object_name = 'promocodes'

    def get_queryset(self):
       
        return PromoCode.objects.filter(
            valid_until__gte=timezone.now(),
            is_active=True
        ).order_by('valid_until')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['archive'] = PromoCode.objects.filter(
            Q(valid_until__lt=timezone.now()) | Q(is_active=False)
        ).order_by('-valid_until')
        return context
    
class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = 'home'

class SignUpView(CreateView): 
    form_class = ClientSignUpForm
    template_name = 'core/signup.html'
    success_url = reverse_lazy('role-based-redirect')

    def form_valid(self, form):
        if not form.is_valid():
            return self.form_invalid(form)
            
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)

class DoctorCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Doctor
    fields = ['full_name', 'cabinet', 'specializations', 'services', 'photo', 'experience']
    template_name = 'core/doctor_form.html'
    
    def test_func(self):
        return self.request.user.is_superuser
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('doctor-detail', kwargs={'pk': self.object.pk})

class DoctorUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Doctor
    fields = ['full_name', 'cabinet', 'specializations', 'services', 'photo', 'experience']
    template_name = 'core/doctor_form.html'
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user == self.get_object().user

class DoctorDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Doctor
    success_url = reverse_lazy('doctors')
    
    def test_func(self):
        return self.request.user.is_superuser
    
class ClientDashboardView(LoginRequiredMixin, TemplateView): 
    template_name = 'core/dashboard_client.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = Appointment.objects.filter(
            client=self.request.user.client
        ).order_by('date_time')
        return context

class UpdateProfileView(LoginRequiredMixin, UpdateView): 
    model = Client
    form_class = ClientProfileForm
    template_name = 'core/update_profile.html'
    success_url = reverse_lazy('client-dashboard')

    def get_object(self):
        return self.request.user.client

    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен')
        return super().form_valid(form)

class DeleteAccountView(LoginRequiredMixin, DeleteView): 
    model = User
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

class DoctorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'core/dashboard_doctor.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        appointments = Appointment.objects.filter(doctor=self.request.user.doctor)
        
        context.update({
            'appointments': appointments.order_by('date_time'),
            'total_patients': appointments.values('client').distinct().count(),
            'completed_appointments': appointments.filter(is_completed=True).count(),
            'upcoming_appointments': appointments.filter(is_completed=False).count()
        })
        return context
    
def role_based_redirect(request):
    if request.user.groups.filter(name='Doctors').exists():
        return redirect('doctor-dashboard')
    elif request.user.groups.filter(name='Clients').exists():
        return redirect('client-dashboard')
    return redirect('home')

class BookAppointmentView(LoginRequiredMixin, CreateView):
    model = Appointment
    form_class = AppointmentForm
    template_name = 'core/book_appointment.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service'] = get_object_or_404(Service, pk=self.kwargs['pk'])
        context['doctors'] = context['service'].doctors.all()
        return context

    def form_valid(self, form):
        service = get_object_or_404(Service, pk=self.kwargs['pk'])
        doctor = get_object_or_404(Doctor, pk=self.request.POST.get('doctor'))
        
        if not doctor.services.filter(pk=service.pk).exists():
            form.add_error(None, "Этот врач не оказывает данную услугу")
            return self.form_invalid(form)
            
        if Appointment.objects.filter(doctor=doctor, date_time=form.cleaned_data['date_time']).exists():
            form.add_error('date_time', "Это время уже занято")
            return self.form_invalid(form)
            
        form.instance.client = self.request.user.client
        form.instance.service = service
        form.instance.doctor = doctor
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('client-dashboard')
    
class ServiceDetailView(DetailView):
    model = Service
    template_name = 'core/service_detail.html'
    context_object_name = 'service'

class CompleteAppointmentView(LoginRequiredMixin, UpdateView):
    model = Appointment
    form_class = CompleteAppointmentForm
    template_name = 'core/complete_appointment.html'
    
    def form_valid(self, form):
        appointment = form.save(commit=False)
        appointment.is_completed = True
        appointment.save()  
        
        Purchase.objects.get_or_create(
            appointment=appointment,
            defaults={
                'service': appointment.service,
                'client': appointment.client,
                'purchase_date': timezone.now()
            }
        )
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse('doctor-dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointment'] = self.get_object()
        return context
    
class StatisticsView(TemplateView):
    template_name = 'core/statistics.html'

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        clients = Client.objects.filter(user__groups__name='Clients')
        context['clients'] = clients.order_by('user__last_name')
        context['age_stats'] = self.get_age_stats(clients)

        services = Service.objects.annotate(
            total_sales=Count('purchase', 
                filter=Q(purchase__appointment__is_completed=True)
            )
        ).filter(total_sales__gt=0).order_by('-total_sales')[:5]

        if services.exists():
            context['chart_data'] = self.prepare_chart_data(services)
            context['pie_chart'] = self.generate_pie_chart(context['chart_data'])
        else:
            context['chart_data'] = None
            context['pie_chart'] = None
        context['purchase_stats'] = self.get_purchase_stats()
        context['line_chart_data'] = self.get_line_chart_data()
        context['line_chart'] = self.generate_line_chart(context['line_chart_data']) \
            if context['line_chart_data']['data'] else None
        service_stats = self.get_service_stats()
        context.update(service_stats)
        return context

    def get_age_stats(self, clients):
        ages = [client.age for client in clients]
        return {
            'average_age': np.mean(ages) if ages else 0,
            'median_age': np.median(ages) if ages else 0
        }

    def prepare_chart_data(self, services):
        return {
            'labels': [s.name for s in services],
            'data': [s.total_sales for s in services],
            'colors': ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
        }

    def generate_pie_chart(self, chart_data):
        try:
            fig = plt.figure(figsize=(6, 6))
            ax = fig.add_subplot(111)
            
            data = [x if x > 0 else 0.1 for x in chart_data['data']]
            total = sum(data)
            
            if total <= 0:
                return None
                
            ax.pie(
                data,
                labels=chart_data['labels'],
                colors=chart_data['colors'],
                autopct=lambda p: f'{p:.1f}%' if p > 0 else ''
            )
            return self.figure_to_base64(fig)
        except Exception as e:
            logger.error(f"Error generating pie chart: {str(e)}")
            return None

    def get_purchase_stats(self):
        purchases = Purchase.objects.filter(
            appointment__is_completed=True
        ).annotate(
            calculated_price=Case(
                When(
                    promo_code__isnull=False,
                    then=F('service__price') * (1 - F('promo_code__discount')/100.0)
                ),
                default=F('service__price'),
                output_field=FloatField() 
            )
        )

        if not purchases.exists():
            return {
                'total_income': 0,
                'average_price': 0,
                'median_price': 0,
                'mode_price': 0
            }

        prices = list(purchases.values_list('calculated_price', flat=True))
        return {
            'total_income': sum(prices),
            'average_price': np.mean(prices) if prices else 0,
            'median_price': np.median(prices) if prices else 0,
            'mode_price': max(set(prices), key=prices.count) if prices else 0
        }

    def get_line_chart_data(self):
        daily_sales = Purchase.objects.filter(
            appointment__is_completed=True
        ).values('purchase_date__date').annotate(
            total=Sum('service__price')
        ).order_by('purchase_date__date')

        labels = []
        data = []
        for item in daily_sales:
            labels.append(item['purchase_date__date'].strftime("%d.%m.%Y"))
            data.append(float(item['total'] or 0))

        return {'labels': labels, 'data': data}

    def get_service_stats(self):
        services = Service.objects.annotate(
            total_purchases=Count(
                'purchase',
                filter=Q(purchase__appointment__is_completed=True)
            )
        ).filter(total_purchases__gt=0)

        service_data = []
        for service in services:
            total_income = Purchase.objects.filter(
                service=service,
                appointment__is_completed=True
            ).annotate(
                final_price=Case(
                    When(
                        promo_code__isnull=False,
                        then=F('service__price') * (1 - F('promo_code__discount')/100.0)
                    ),
                    default=F('service__price'),
                    output_field=FloatField()
                )
            ).aggregate(total=Sum('final_price'))['total'] or 0

            service_data.append({
                'object': service,
                'total_income': total_income
            })

        most_popular = max(services, key=lambda x: x.total_purchases, default=None)
        most_profitable = max(service_data, key=lambda x: x['total_income'], default=None)

        return {
            'most_popular': most_popular,
            'most_profitable': most_profitable['object'] if most_profitable else None,
            'most_profitable_income': most_profitable['total_income'] if most_profitable else 0
        }

    def figure_to_base64(self, figure):
        buffer = BytesIO()
        figure.savefig(buffer, format='png', bbox_inches='tight')
        plt.close(figure)
        plt.close('all')
        return base64.b64encode(buffer.getvalue()).decode('utf-8')
    
    def generate_line_chart(self, line_data):
        try:
            if not line_data['data']:
                return None
                
            fig = plt.figure(figsize=(8, 4))
            ax = fig.add_subplot(111)
            ax.set_title("Динамика продаж по дням")
            ax.plot(line_data['labels'], line_data['data'], marker='o')
            ax.set_xlabel('Дата')
            ax.set_ylabel('Доход (руб.)')
            plt.xticks(rotation=45)
            ax.grid(True)
            fig.tight_layout()
            return self.figure_to_base64(fig)
        except Exception as e:
            logger.error(f"Ошибка генерации линейного графика: {str(e)}")
            return None

def set_timezone(request):
    if request.method == 'POST':
        form = TimezoneForm(request.POST)
        if form.is_valid():
            request.session['user_timezone'] = form.cleaned_data['timezone']
            messages.success(request, 'Временная зона успешно обновлена')
            request.session.modified = True
            return redirect('home')
    else:
        initial = request.session.get('user_timezone', 'UTC')
        form = TimezoneForm(initial={'timezone': initial})
    
    return render(request, 'core/set_timezone.html', {'form': form})

