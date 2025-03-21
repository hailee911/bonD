from django.db import models
from loginpage.models import Member
from django.core.exceptions import ValidationError

# 개인 다이어리 테이블
class MdiaryBoard(models.Model):
  mno = models.AutoField(primary_key=True)
  id = models.ForeignKey(Member,on_delete=models.DO_NOTHING, null=True)
  mtitle = models.CharField(max_length=1000,default='나의 일기장')
  mdate = models.DateField(auto_now=True)

  def __str__(self):
    return f"{self.mno},{self.id.id},{self.id.nicName},{self.mtitle},{self.mdate}"
  

# 우체통
from loginpage.models import Member
class Letter(models.Model):
  lno = models.AutoField(primary_key=True)
  member = models.ForeignKey(Member,on_delete=models.DO_NOTHING, null=True)
  ltitle = models.CharField(max_length=1000)
  lcontent = models.TextField()
  ldate = models.DateTimeField(auto_now=True)
  lhit = models.IntegerField(default=0)

  def __str__(self):
    return f"{self.lno},{self.member},{self.ltitle},{self.lcontent},{self.ldate}"
  

# 그룹 다이어리 db 나중에 그룹 다이어리 생성 시 중복 체크해서 raise ValidationError("이미 그룹 다이어리가 존재합니다.")
# 한 아이디가 하나의 그룹 다이어리 생성 할 수 있도록
class GroupDiary(models.Model):
  gno = models.IntegerField(default=0, null=False)
  member = models.ForeignKey(Member,on_delete=models.DO_NOTHING, null=False)
  gtitle = models.CharField(max_length=200)
  gName = models.CharField(max_length=100, null=False, default="우리 가족") # 그룹이름
  created_at = models.DateTimeField(auto_now_add=True)
  role = models.IntegerField(default=1)
  
  def __str__(self):
    return f"{self.gno},{self.member.id},{self.gtitle},{self.gName},{self.created_at}"

  # def clean(self):
  #   # 같은 사용자가 이미 그룹 다이어리를 생성한 경우 ValidationError 발생
  #   if GroupDiary.objects.filter(member=self.member).exists():
  #       raise ValidationError("이미 그룹 다이어리가 존재합니다.")
    

# 다이어리 작성 -> 내용 db
from django.utils import timezone
class Content(models.Model):
  cno = models.AutoField(primary_key=True)
  member = models.ForeignKey(Member,on_delete=models.DO_NOTHING, null=False) # 유저id & 닉네임 가져옴
  ctitle = models.CharField(max_length=1000)
  ccontent = models.TextField(null=True)
  cdate = models.DateTimeField(default=timezone.now)  # 기본값을 오늘 날짜로 설정
  group_diary  = models.ManyToManyField(GroupDiary, blank=True)
  # 공용다이어리 db 만들면 추후 업데이트
  image = models.ImageField(upload_to='diary_images/', blank=True, null=True)  # 이미지
  # 개인다이어리 db
  mdiary = models.ForeignKey(MdiaryBoard, on_delete=models.CASCADE, null=True, blank=True)
  def __str__(self):
    group_diaries = ", ".join([str(diary) for diary in self.group_diary.all()])
    return f"{self.cno}, {self.member.id}, {self.ctitle}, {self.ccontent}, {self.cdate}, [{group_diaries}], {self.member.nicName}"


