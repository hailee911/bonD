from django.contrib import admin
from diary.models import MdiaryBoard

@admin.register(MdiaryBoard)
class MdiaryBoardAdmin(admin.ModelAdmin):
    list_display = ['mno','id','get_nicName', 'mtitle', 'mdate']

    # 커스텀 메서드 정의
    def get_nicName(self, obj):
        return obj.id.nicName if obj.id and hasattr(obj.id, 'nicName') else None

    # list_display에서 보이는 이름 설정
    get_nicName.short_description = '닉네임'
  


# 우체통
from diary.models import Letter

@admin.register(Letter)
class LetterAdmin(admin.ModelAdmin):
    list_display = ['lno','member','ltitle','lcontent','ldate']
    

# 그룹다이어리 & 내용
from diary.models import GroupDiary,Content    
@admin.register(GroupDiary)
class GroupDiaryAdmin(admin.ModelAdmin):
    list_display = ['gno','member_id','gtitle','gName','created_at']
    
from django.contrib import admin
from .models import Content

@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ['cno', 'member_id', 'ctitle', 'ccontent', 'cdate', 'get_group_diaries', 'member_nicName']
    def get_group_diaries(self, obj):
        # ManyToMany 관계 데이터를 콤마로 구분된 문자열로 반환
        return ", ".join([diary.gName for diary in obj.group_diary.all()])
    get_group_diaries.short_description = 'Group Diaries'  # Admin에서 컬럼 헤더로 표시할 이름
    # member_nicName을 반환하는 메서드 정의
    def member_nicName(self, obj):
        return obj.member.nicName if obj.member else None
    # member_nicName으로 정렬 가능하게 설정
    member_nicName.admin_order_field = 'member__nicName'
    # 컬럼 제목 설정
    member_nicName.short_description = 'Member Nickname'
