from django.db import models
from loginpage.models import Member
from diary.models import Content

class Like(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE, null=True, blank=True)  # Content와 연결
    liked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member.name},{self.content} at {self.liked_at}"
