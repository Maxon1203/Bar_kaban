
from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User

class CustomUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    avatar = models.ImageField(blank=True, verbose_name="Аватар", upload_to='image/')
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации", blank=True, null=True)

    def __str__(self):
        return self.user.username

class Bar(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    address = models.CharField(max_length=255, verbose_name="Адрес")
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")
    description = models.TextField(verbose_name="Описание")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    website = models.URLField(blank=True, verbose_name="Веб-сайт")
    image = models.ImageField(upload_to='image/bars/', verbose_name='Фотография бара', blank=True)
    users_liked = models.ManyToManyField(CustomUser, related_name='liked_bars', blank=True)

    def review_srednee(self):
        reviews = self.review_set.all()
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        return average_rating or 0

    def __str__(self):
        return self.name

class Festival(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(verbose_name="Описание")
    date = models.DateField(verbose_name="Дата проведения")
    location = models.CharField(max_length=255, verbose_name="Место проведения")
    website = models.URLField(blank=True, verbose_name="Веб-сайт")

    def __str__(self):
        return self.name

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Пользователь")
    bar = models.ForeignKey(Bar, on_delete=models.CASCADE, verbose_name="Бар")
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)], verbose_name="Оценка")
    comment = models.TextField(verbose_name="Комментарий")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Дата отзыва")


    def __str__(self):
        return f"Отзыв от {self.user.registration_date} для {self.bar.name}"
