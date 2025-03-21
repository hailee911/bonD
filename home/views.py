from django.shortcuts import render, redirect
from loginpage.models import Member
from diary.models import Content
from diary.models import MdiaryBoard
from diary.models import GroupDiary
from customer.models import NoticeBoard
from emotion.models import EmotionScore
from mypage.models import Img
from django.http import JsonResponse
from django.db.models import Q
from datetime import datetime, timedelta
from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
from notifications.models import Notification

# 랜딩페이지
def landing(request):
  return render(request,'landing.html')

def main(request):
  id = request.session['session_id']
  # 내정보
  qs = Member.objects.filter(id=id).first()
  # 내 프사
  qb = Img.objects.filter(id=id).first()
  # 포스트
  qs_post = NoticeBoard.objects.filter(category=2).order_by('-bno')
  # 내 다이어리
  my_diary = MdiaryBoard.objects.filter(id=id).first()

  # 최신 일상들
  if qs.created_group == None and qs.joined_group == None:
    daily_new = '공유 일기장을 만들어 보세요!'
  else:
    if qs.created_group and qs.joined_group == None:
        g1 = GroupDiary.objects.filter(gno=qs.created_group.gno).first()
        groups = [g1]
    elif qs.created_group == None and qs.joined_group:
        g2 = GroupDiary.objects.filter(gno=qs.joined_group.gno).first()
        groups = [g2]
    else:
        g1 = GroupDiary.objects.filter(gno=qs.created_group.gno).first()
        g2 = GroupDiary.objects.filter(gno=qs.joined_group.gno).first()
        groups = [g1,g2]
    # 사용자가 작성한 글을 제외하고, 해당 그룹들의 콘텐츠를 최신순으로 가져옵니다.
    daily_new = Content.objects.filter(
        group_diary__in=groups  # 가입된 그룹 + 만든 그룹
    ).exclude(member=qs)  # 사용자가 작성한 글 제외
    daily_new = daily_new.distinct().order_by('-cdate')[:5]
    if not daily_new.exists():
        daily_new = '가족들의 최근 소식이 없어요. 오늘의 기록을 가족이 볼 수 있게 공유해보세요.'

  # 과거의 오늘
  # 1년 전 오늘 날짜 계산
  today = timezone.localtime(timezone.now()).date()
  year_ago = today.replace(year=today.year - 1)

  # 1년 전 오늘 날짜에 작성된 일기를 필터링
  past = Content.objects.filter(
      member = qs,
      cdate__date=year_ago  # 1년 전 오늘 날짜와 같은 날짜의 일기만 가져오기
    ).first()

  context = {'post_lists':qs_post,
              'my':qs, 
              'my_img':qb,
              'my_diary':my_diary,
              'daily_new':daily_new,
              'past':past,
              }
  return render(request, 'main.html', context)

def logout(request):
  request.session.clear()
  return redirect('/')

# 검색창
def search(request):
  id = request.session['session_id']
  csearch = request.POST.get("csearch")
  print("csearch : ",csearch)
  member = Member.objects.get(id=id)
  qs = list(Content.objects.filter(Q(member=member,ctitle__contains=csearch)|Q(member=member,ccontent__contains=csearch) ).values())
  print("qs : ",qs)
  context = {"list_qs":qs}
  return JsonResponse(context)

# 우리가족 데려오기
def get_family_members(request):
    id = request.session['session_id']
    qs = Member.objects.filter(id=id).first()
    
    # 가입된 그룹이 없을 때
    if qs.created_group == None and qs.joined_group == None:
        return JsonResponse(data, safe=False)
    
    # 만든 그룹만 있을 때
    else:
        if qs.created_group and qs.joined_group == None:
            my_cdi = qs.created_group.gno

            # 가족 구성원의 이름을 가져옵니다.
            family_members = GroupDiary.objects.filter(gno=my_cdi)
            unique_members = {}
            for member in family_members:
                unique_members[member.member.id] = member.member.name  # 중복 제거

            # 내 이름을 가장 먼저 추가
            my_name = qs.name  # 내 이름
            data = [{'id': qs.id, 'name': my_name}]  # 내 이름을 먼저 추가

            # 내 이름을 제외한 나머지 가족 구성원들 추가
            for member_id, name in unique_members.items():
                if member_id != qs.id:
                    data.append({'id': member_id, 'name': name})
        
        # 가입된 그룹만 있을 때
        elif qs.joined_group and qs.created_group == None:
            my_jdi = qs.joined_group.gno
            # 가족 구성원의 이름을 가져옵니다.
            family_members = GroupDiary.objects.filter(gno=my_jdi)
            unique_members = {}
            for member in family_members:
                unique_members[member.member.id] = member.member.name  # 중복 제거

            # 내 이름을 가장 먼저 추가
            my_name = qs.name  # 내 이름
            data = [{'id': qs.id, 'name': my_name}]  # 내 이름을 먼저 추가

            # 내 이름을 제외한 나머지 가족 구성원들 추가
            for member_id, name in unique_members.items():
                if member_id != qs.id:
                    data.append({'id': member_id, 'name': name})
    
        # 둘 다 있을 때
        else:
            my_cdi = qs.created_group.gno
            my_jdi = qs.joined_group.gno

            # 가족 구성원의 이름을 가져옵니다.
            family_members = GroupDiary.objects.filter(Q(gno=my_cdi) | Q(gno=my_jdi))
            unique_members = {}
            for member in family_members:
                unique_members[member.member.id] = member.member.name  # 중복 제거

            # 내 이름을 가장 먼저 추가
            my_name = qs.name  # 내 이름
            data = [{'id': qs.id, 'name': my_name}]  # 내 이름을 먼저 추가

            # 내 이름을 제외한 나머지 가족 구성원들 추가
            for member_id, name in unique_members.items():
                if member_id != qs.id:
                    data.append({'id': member_id, 'name': name})

    return JsonResponse(data, safe=False)

# 우리가족 데이터 가져오기
def get_emotion_graph(request, member_id):
    current_date = datetime.today()
    weekday = current_date.weekday()  # 현재 요일 계산
    monday_date = current_date - timedelta(days=weekday)  # 월요일 날짜
    sunday_date = monday_date + timedelta(days=6)  # 일요일 날짜

    # 이번 주의 월요일부터 일요일까지 날짜 리스트
    week_dates = [monday_date + timedelta(days=i) for i in range(7)]
    weekdays = ["월", "화", "수", "목", "금", "토", "일"]

    # EmotionScore 모델에서 해당 주의 감정 점수 가져오기
    emotion_data = EmotionScore.objects.filter(
        member_id=member_id,
        diarydate__gte=monday_date,
        diarydate__lte=sunday_date
    ).values('diarydate', 'emotionscore')

    # 날짜별 감정 점수 평균값 계산
    grouped_data = {}
    for entry in emotion_data:
        diary_date = entry['diarydate']
        emotion_score = entry['emotionscore']
        
        if diary_date in grouped_data:
            grouped_data[diary_date].append(emotion_score)
        else:
            grouped_data[diary_date] = [emotion_score]
    
    # 평균값 계산
    averaged_data = {}
    for date, scores in grouped_data.items():
        averaged_data[date] = sum(scores) / len(scores)  # 평균값 계산

    # 결과 데이터 생성
    data = []
    for date in week_dates:
        day_of_month = date.day
        day_label = weekdays[date.weekday()]
        
        # datetime.date 객체를 비교할 수 있도록 동일한 형식으로 변환
        value = averaged_data.get(date.date(), 0)  # 해당 날짜의 평균 감정 점수, 없으면 0
        data.append({
            "name": str(day_of_month),  # 일(day)
            "label": day_label,  # 요일
            "value": value,  # 평균 감정 점수
        })

    # JSON 응답으로 반환
    return JsonResponse(data, safe=False)





## 알림창
def notification_list(request):
    # 현재 로그인한 사용자 ID
    user_id = request.session.get('session_id')
    if not user_id:
        return JsonResponse({'error': '로그인 필요'}, status=403)

    # 알림 데이터 가져오기
    notifications = Notification.objects.filter(user_id=user_id).order_by('-ndate')
    notification_list = [{
        'id': n.id,  # 여기에 ID를 포함시킵니다.
        'message': n.message,
        'checked': n.checked,
        'ndate': n.ndate.strftime('%Y-%m-%d %H:%M:%S')
    } for n in notifications]

    return JsonResponse({'notifications': notification_list})



def notification_read(request, notification_id):
    if request.method == "POST":
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.checked = True
            notification.save()
            return JsonResponse({'status': 'success'})
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Notification not found.'}, status=404)
    return JsonResponse({'status': 'error', 'message': 'Invalid request method.'}, status=400)


