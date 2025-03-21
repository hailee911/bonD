from django.db import models


# 알림 db
class Notification(models.Model):

	user_id = models.CharField(max_length=50)  			  # session_id로 날릴거임
	message = models.TextField()  										# 알림 메시지
	checked = models.BooleanField(default=False)  		# 읽음 여부
	ndate = models.DateTimeField(auto_now_add=True)
	
	def __str__(self):
		return f"{self.user_id},{self.message},{self.checked},{self.ndate}"