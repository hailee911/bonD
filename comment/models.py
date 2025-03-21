from django.db import models
from loginpage.models import Member
from diary.models import Content

# 댓글 모델
class Comment(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)  # 연결된 게시글
    member = models.ForeignKey(Member, on_delete=models.CASCADE)  # 작성자
    text = models.TextField()  # 댓글 내용
    created_at = models.DateTimeField(auto_now_add=True)  # 댓글 작성 시간
    updated_at = models.DateTimeField(auto_now=True)  # 댓글 수정 시간
    group_num = models.IntegerField(null=True)  # 해당 다이어리의 group_num (created_group 또는 joined_group의 gno)

    def __str__(self):
        return f"{self.member.name} - {self.text[:20]}, {self.group_num}"
