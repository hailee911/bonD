from django.db import models
from loginpage.models import Member
from admin1.models import Administrator

# 공지사항/포스트 
class NoticeBoard(models.Model):
  bno = models.AutoField(primary_key=True)
  # do_nothing : 아무것도 하지 않음 ( 자식의 값이 다 지워져야 부모도 지울 수 있음 [default] )
  # cascade : 외래키를 포함하는 행도 함께 삭제 (부모 지울 때 자식도 다 지움)
  # protect : 해당 요소가 함께 삭제되지 않도록 오류 발생
  # set_null : 외래키 값을 null로 변경 (부모를 지우면 자식의 있는 모든 내용을 null)
  member = models.ForeignKey(Administrator,on_delete=models.SET_NULL, null=True)
  btitle = models.CharField(max_length=1000)
  bcontent = models.TextField()
  bdate = models.DateTimeField(auto_now_add=True)

  # img파일 업로드
  bfile = models.ImageField(null=True, blank=True, upload_to='uploads/')
  bfile_thumbnail = models.ImageField(null=True, blank=True, upload_to='uploads/')
  userid = models.CharField(max_length=100,null=True, blank=True)
  bmail = models.CharField(max_length=100, null=True, blank=True)
  category = models.IntegerField(null=True, blank=False)
  status = models.CharField(max_length=50, null=True, blank=True)


  def __str__(self):
    return f'{self.bno}, {self.btitle}, {self.bdate}'
  

