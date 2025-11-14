from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, RegexValidator, MaxValueValidator
from django.core.exceptions import ValidationError
import datetime
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import Group
import pytz
from django.db.models import Count, Sum, Avg
import statistics
from django.db.models import F, Case, When, FloatField   
from django.db.models import Q

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='client')
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+375 \(\d{2}\) \d{3}-\d{2}-\d{2}$',
                message="Номер должен быть в формате +375 (29) XXX-XX-XX"
            )
        ]
    )
    birth_date = models.DateField()
    address = models.TextField()
    
    @property
    def age(self):
        return (datetime.date.today() - self.birth_date).days // 365
    
    def clean(self):
        if self.age < 18:
            raise ValidationError("Клиент должен быть старше 18 лет")
        
    @classmethod
    def get_age_stats(cls):
        # filter only users - 'Clients'
        clients = cls.objects.filter(user__groups__name='Clients')
        ages = [client.age for client in clients]
        return {
            'average_age': statistics.mean(ages) if ages else 0,
            'median_age': statistics.median(ages) if ages else 0
        }
    

class Cabinet(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Specialization(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    specializations = models.ManyToManyField(Specialization)
    cabinet = models.ForeignKey(Cabinet, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=50)
    photo = models.ImageField(upload_to='doctors/', blank=True, null=True) 
    experience = models.PositiveIntegerField(verbose_name="Опыт работы (лет)") 
    full_name = models.CharField(max_length=200, verbose_name="Полное ФИО")  
    start_date = models.DateField(verbose_name="Дата начала практики", default=timezone.now)  
    services = models.ManyToManyField(
        'Service',
        related_name='doctors',
        verbose_name='Оказываемые услуги'
    )
    phone = models.CharField(
        max_length=20,
        validators=[
            RegexValidator(
                regex=r'^\+375\(\d{2}\)\d{3}-\d{2}-\d{2}$',
                message="Номер должен быть в формате +375 (29) XXX-XX-XX"
            )
        ],
        verbose_name="Телефон"
    )
    email = models.EmailField(verbose_name="Email")

    @property
    def experience_calculated(self):
        """Автоматический расчет стажа на основе даты начала"""
        today = timezone.now().date()
        delta = today - self.start_date
        return delta.days // 365

    def __str__(self):
        return self.full_name
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        doctors_group = Group.objects.get(name='Doctors')
        clients_group = Group.objects.get(name='Clients')
        self.user.groups.add(doctors_group)
        self.user.groups.remove(clients_group)

class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    short_description = models.CharField(
        max_length=200, 
        verbose_name="Краткое описание"
    )
    full_description = models.TextField(verbose_name="Полное описание")
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Стоимость"
    )
    duration = models.DurationField(verbose_name="Продолжительность")
    
    def duration_formatted(self):
        total_seconds = int(self.duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        return f"{hours:02d}:{minutes:02d}" if hours > 0 else f"{minutes} мин."

    def __str__(self):
        return self.name
    
    @classmethod
    def get_service_stats(cls):
        services = cls.objects.annotate(
            total_purchases=Count(
                'purchase',
                filter=Q(purchase__appointment__is_completed=True) 
            ),
            total_income=Sum(
                Case(
                    When(
                        purchase__appointment__is_completed=True,  
                        purchase__promo_code__isnull=False,
                        then=F('price') * (1 - F('purchase__promo_code__discount')/100.0 )
                    ),
                    default=F('price'),
                    output_field=FloatField()
                )
            )
        ).order_by('-total_purchases')
    
        return {
            'most_popular': services.first() if services else None,
            'most_profitable': services.order_by('-total_income').first() if services else None
        }

class Appointment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    date_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False, verbose_name="Завершен") 
    doctor_notes = models.TextField(blank=True, null=True, verbose_name="Комментарий врача") 

    def __str__(self):
        return f"{self.client.user.get_full_name()} - {self.service.name} ({self.date_time})"



class Review(models.Model):
    RATING_CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        verbose_name="Пользователь"
    )
    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Оценка"
    )
    text = models.TextField(verbose_name="Текст отзыва")
    date = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Дата публикации"
    )

    class Meta:
        ordering = ['-date']
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return f"Отзыв от {self.user.username}"

class PromoCode(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name="Код")
    discount = models.PositiveIntegerField(verbose_name="Скидка (%)")
    valid_until = models.DateField(verbose_name="Действует до")
    is_active = models.BooleanField(default=True, verbose_name="Активен")

    class Meta:
        ordering = ['-valid_until']
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'

    def __str__(self):
        return f"{self.code} ({self.discount}%)"




class Cart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    is_checked_out = models.BooleanField(default=False)
    promo_code = models.ForeignKey(PromoCode, on_delete=models.SET_NULL, null=True, blank=True)

    def total_price(self):
        total = sum(item.total_price() for item in self.items.all())
        if self.promo_code and self.promo_code.is_active:
            total *= (1 - self.promo_code.discount / 100)
        return round(total, 2)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True, blank=True)
    date_time = models.DateTimeField(null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price_at_addition = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def total_price(self):
        return self.quantity * self.price_at_addition


class Payment(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name="Корзина"
    )
    cart_item = models.ForeignKey(
        CartItem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Услуга в корзине"
    )
    paid_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата оплаты"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Сумма"
    )
    method = models.CharField(
        max_length=50,
        choices=[
            ('card', 'Карта'),
            ('cash', 'Наличные'),
            ('online', 'Онлайн')
        ],
        verbose_name="Способ оплаты"
    )

    # 🔐 Новые поля для логирования карты
    card_last4 = models.CharField(
        max_length=4,
        blank=True,
        null=True,
        verbose_name="Последние 4 цифры карты"
    )
    card_holder = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Имя владельца карты"
    )

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"
        ordering = ['-paid_at']

    def __str__(self):
        return f"{self.method} — {self.amount} руб. ({self.paid_at.strftime('%d.%m.%Y')})"



class News(models.Model):
    title = models.CharField(max_length=200)
    short_content = models.CharField(max_length=200)
    full_content = models.TextField()
    image = models.ImageField(upload_to='news/')
    publish_date = models.DateTimeField(auto_now_add=True)

class Partner(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название компании")
    logo = models.ImageField(upload_to='partners/', verbose_name="Логотип")
    website = models.URLField(verbose_name="Сайт компании")

    class Meta:
        verbose_name = "Партнёр"
        verbose_name_plural = "Партнёры"

    def __str__(self):
        return self.name

class CompanyInfo(models.Model):
    name = models.CharField("Название компании", max_length=255)
    description = models.TextField("Описание")
    founded = models.DateField("Дата основания")
    employees = models.PositiveIntegerField("Количество сотрудников")
    website = models.URLField("Сайт", blank=True)

    logo = models.ImageField("Логотип", upload_to="company/", blank=True, null=True)
    video_url = models.URLField("Видео о компании", blank=True)

    history = models.TextField("История по годам", blank=True)
    requisites = models.TextField("Реквизиты", blank=True)
    certificate = models.TextField("Сертификат", blank=True)

    class Meta:
        verbose_name = "Информация о компании"
        verbose_name_plural = "Информация о компании"

    def __str__(self):
        return self.name

class GlossaryTerm(models.Model):
    term = models.CharField(max_length=200, verbose_name="Термин")
    definition = models.TextField(verbose_name="Определение")
    date_added = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")

    class Meta:
        ordering = ['-date_added']
        verbose_name = 'Термин'
        verbose_name_plural = 'Глоссарий'

    def __str__(self):
        return self.term

class Employee(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='employees/')
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    description = models.TextField()

class Vacancy(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    date_posted = models.DateField(
        auto_now_add=True, 
        verbose_name="Дата публикации"
    )

    class Meta:
        verbose_name = "Вакансия"
        verbose_name_plural = "Вакансии"
        ordering = ['-date_posted']

    def __str__(self):
        return self.title

class Purchase(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ForeignKey(
        'Service',
        on_delete=models.CASCADE,
        related_name='purchase'  
    )
    purchase_date = models.DateTimeField(auto_now_add=True)
    used = models.BooleanField(default=False)
    promo_code = models.ForeignKey(PromoCode, null=True, blank=True, on_delete=models.SET_NULL)
    appointment = models.OneToOneField(
        'Appointment',
        on_delete=models.CASCADE,
        related_name='purchase',
        verbose_name="Связанная запись"
    )
    @classmethod
    def get_financial_stats(cls):
        purchases = cls.objects.filter(
            appointment__is_completed=True
        ).annotate(
            calculated_price=Case(
                When( 
                    promo_code__isnull=False,
                    then=F('service__price') * (1 - F('promo_code__discount')) / 100.0
                ),
                default=F('service__price'),
                output_field=FloatField()
            )
        )

        prices = list(purchases.values_list('calculated_price', flat=True))
        print("[DEBUG] Prices for mode calculation:", prices)
        if not prices:
            return {
                'total_income': 0,
                'average_price': 0,
                'median_price': 0,
                'mode_price': 0
            }
        
        modes = statistics.multimode(prices)
        if len(modes) == len(prices):
        # all values 1 time → mode isn't
            mode_price = 0
        else:
        # first mode of list
            mode_price = modes[0] if modes else 0
    
        return {
            'total_income': sum(prices),
            'average_price': statistics.mean(prices),
            'median_price': statistics.median(prices),
            'mode_price': mode_price
        }
    
class GroupProxy(Group):
    class Meta:
        proxy = True
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    timezone = models.CharField(
        max_length=50, 
        choices=[(tz, tz) for tz in pytz.all_timezones], 
        default='UTC',
        blank=False   
    )
    
    def __str__(self):
        return f"Профиль {self.user.username}"