from django.db import models

# import datetime
from datetime import datetime
class Member(models.Model):
  id = models.CharField(max_length=50,primary_key=True)
  pw = models.CharField(max_length=100)
  name = models.CharField(max_length=100)
  nicName = models.CharField(max_length=100,default='123')
  mail = models.EmailField(max_length=100)
  birthday = models.CharField(max_length=50)
  gender = models.CharField(max_length=10,choices=[('남자', '남자'), ('여자', '여자')])
  mdate = models.DateTimeField(auto_now=True)
  # mdate = models.DateTimeField(default=datetime.now())
  # 테스트
  created_group = models.OneToOneField(
        'diary.GroupDiary',  # '앱이름.모델이름' 형식
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='creator'
    )
  joined_group = models.ForeignKey(
        'diary.GroupDiary',  # '앱이름.모델이름' 형식
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='members'
    )
  

  def __str__(self):
    return f"{self.id},{self.name},{self.mdate}"