from django.shortcuts import render, redirect
from loginpage.models import Member
from mypage.models import Img
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from django.db import IntegrityError


@csrf_exempt
def profile_upload(request):
    if request.method == "POST":
        user_id = request.session['session_id']  # 현재 세션의 사용자 ID
        user_img = Img.objects.get(id=user_id)  # 해당 ID에 맞는 객체 불러오기

        uploaded_file = request.FILES.get('file')  # 업로드된 파일 가져오기
        if uploaded_file:
            user_img.img = uploaded_file  # 이미지 필드 업데이트
            user_img.save()  # DB에 저장
            return redirect('/mypage/main/')  # 완료 후 마이페이지로 리다이렉트
        else:
            return HttpResponse("파일 업로드 실패", status=400)
    return HttpResponse("잘못된 요청", status=400)


# Create your views here.
def main(request):
  id = request.session['session_id']
  qs = Member.objects.filter(id=id)
  qb = Img.objects.filter(id=id).first()
  # 생년월일을 8자리 문자열로 받았다 가정
  formatted_birth_date = qs[0].birthday

  # 문자열 슬라이싱을 통해 년, 월, 일을 분리하고 점으로 구분

  print(formatted_birth_date)  # 결과: 1990.12.31

  context = {'my':qs[0], 'my_birth':formatted_birth_date, "qb":qb
             }
  return render(request, 'mymain.html', context)

def modify(request):
  # 회원 정보 수정 불러오기
  id = request.session['session_id']
  qs = Member.objects.filter(id=id)
  if request.method == 'GET':
    qb = Img.objects.filter(id=id).first()
    email = qs[0].mail.split('@')
    context = {'mem_info':qs[0], 'mail_id':email[0], 'mail_domain':email[1], 'qb':qb}
    return render(request, 'mypage_modi.html', context)
  
  # 바뀐 정보 불러오기 및 저장
  else:
    nicName = request.POST.get('mypage_nicname')
    mail_id = request.POST.get('mypage_mailid')
    mail_domain = request.POST.get('mypage_email2')
    gender = request.POST.get('mypage_gender')
    birthday = request.POST.get('mypage_birth')
    print(nicName)

    qs.update(
    nicName = nicName,
    mail = f'{mail_id}@{mail_domain}',
    gender = gender,
    birthday = birthday
    )

    print('post : ',qs[0].nicName)
    return redirect('/mypage/main/')

# 회원정보 수정 > 현재 비밀번호 확인
def currpw_chk(request):
  id = request.session['session_id']
  pw = request.POST.get('currPw','')
  qs = Member.objects.filter(pw=pw, id=id)
  
  if qs:
    context = {'result':'success'}
  else:
    context = {'result':'fail'}
    print('에러')

  return JsonResponse(context) 

# 회원정보 수정 > 비밀번호 변경
def pw_chg(request):
  id = request.session['session_id']
  newPw = request.POST.get('newPw')
  qs = Member.objects.get(id=id)
  print(qs.pw)
  qs.pw = newPw
  qs.save()
  print(qs.pw)
  return JsonResponse({'result': 'success'})

def delaccount(request):
    # 세션에서 현재 로그인한 회원의 ID 가져오기
    id = request.session['session_id']

    # 해당 회원 객체를 가져오기
    try:
        qs = Member.objects.get(id=id)
        print('삭제 전 : ', qs)
        
        # 해당 회원과 관련된 데이터 삭제
        qs.letter_set.all().delete()  # 우체통 데이터 삭제
        qs.mdiaryboard_set.all().delete()  # 개인 다이어리 삭제
        qs.groupdiary_set.all().delete()  # 그룹 다이어리 삭제
        qs.content_set.all().delete()  # 다이어리 내용 삭제
        qs.emotionscore_set.all().delete()  # 다이어리 내용 삭제
        
        # 마지막으로 회원 삭제
        qs.delete()
        print('삭제 후 : ', qs)
        # 세션 삭제 후 홈페이지로 리다이렉트
        del request.session['session_id']  # 세션 삭제
        request.session.clear()
        
        # 세션 종료 후 홈페이지로 리다이렉트
        return redirect('/')
    except Member.DoesNotExist:
        return redirect('/')  # 만약 해당 회원이 없으면 리다이렉트
    except IntegrityError:
        return redirect('/')  # 외래 키 제약 등으로 인한 오류 처리