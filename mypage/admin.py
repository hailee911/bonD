from django.contrib import admin
from .models import Img

# Register your models here.
class ImgAdmin(admin.ModelAdmin):
    list_display = ('id', 'img_thumbnail')  # 이미지 썸네일을 보여줄 함수 추가
    
    # 이미지 썸네일을 보여주는 함수
    def img_thumbnail(self, obj):
        if obj.img:
            return f'<img src="{obj.img.url}" width="50" height="50" />'
        else:
            # 이미지가 없으면 디폴트 이미지 표시
            return f'<img src="../static/images/calendar1/default_profile.png" width="50" height="50" />'
    img_thumbnail.allow_tags = True  # HTML 태그를 렌더링 가능하게 설정

admin.site.register(Img, ImgAdmin)