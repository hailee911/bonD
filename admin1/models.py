from django.db import models


class Administrator(models.Model):
  ano = models.IntegerField(default=0)
  id = models.CharField(max_length=50,primary_key=True)
  pw = models.CharField(max_length=100)
  name = models.CharField(max_length=100)
  nickname = models.CharField(max_length=100,default='관리자')
  tel = models.CharField(max_length=20,default='010-0000-0000')
  role = models.IntegerField()
  adate = models.DateTimeField(auto_now=True)
  
  def __str__(self):
    return f"{self.id},{self.name},{self.role}"