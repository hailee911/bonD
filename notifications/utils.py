from .models import Notification

# 알림생성 함수
# id,message 등록하면됨.
def create_notification(user_id, message):
    # """
    # 알림을 생성하는 함수
    # :param user_id: 알림을 받을 사용자 ID (session_id 기준)
    # :param message: 알림 내용
    # """

    Notification.objects.create(
        user_id=user_id,
        message=message
    )