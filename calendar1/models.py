from django.db import models
from loginpage.models import Member


class Event(models.Model):
    # 고유번호는 자동 증가하는 IntegerField
    no = models.AutoField(primary_key=True)  # AutoField는 자동으로 증가하는 고유번호
    
    # 작성자 이름은 Member 모델과 ForeignKey로 연결
    name = models.ForeignKey(Member, on_delete=models.CASCADE,null=True)  # 작성자는 다른 모델에서 가져옵니다
    color = models.CharField(max_length=100, default='#0000FF')  # 색상 필드 (기본값 파란색)
    title = models.CharField(max_length=255,null=True, default="제목이없습니다.")  # 제목
    start_date = models.DateTimeField(null=True)  # 시작 시간
    end_date = models.DateTimeField(null=True)  # 종료 시간
    location = models.CharField(max_length=255, default="장소가 없습니다.")  # 장소, 빈 값 허용
    repeat = models.CharField(max_length=20, choices=[('none', '없음'), ('daily', '매일'), ('weekly', '매주'), ('monthly', '매월'), ('yearly', '매년')], default='none')
    memo = models.TextField(default="내용이없습니다.")  # 메모, 빈 값 허용
    created_at = models.DateTimeField(auto_now_add=True)  # 생성일, 생성 시 자동 저장
    
    def __str__(self):
        return self.title