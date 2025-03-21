from django.db import models

# Create your models here.
class Img(models.Model):
  id = models.CharField(max_length=50, primary_key=True)  # 고유한 ID
  img = models.ImageField(upload_to='images/', null=True, blank=True, default='../static/images/calendar1/default_profile.png')  # 디폴트 이미지 설정

  def __str__(self):
    return f"ID: {self.id}, Image: {self.img}"