from django.db import models


# Модель для страниц сайта
class Topics(models.Model):
    name = models.CharField(max_length=100, unique=True)
    url = models.CharField(max_length=100, unique=True, null=True)

    def __str__(self):
        return self.name


# Модель для публикаций
class Publication(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    publish_date = models.DateTimeField(auto_now_add=True)
    page = models.ForeignKey(Topics, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return self.title

