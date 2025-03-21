from django.db import models
from loginpage.models import Member

from datetime import date
class EmotionScore(models.Model):
  member = models.ForeignKey(Member,on_delete=models.DO_NOTHING, null=True)
  # diaryNo = models.ForeignKey(일기내용 클래스)
  diaryNo = models.IntegerField(default=0)
  diarydate = models.DateField(default=date.today)
  emotionscore = models.IntegerField(default=0)

  def __str__(self):
    return f"{self.member}, {self.emotionscore}"