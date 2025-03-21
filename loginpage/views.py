from django.shortcuts import render,redirect
from loginpage.models import Member
from mypage.models import Img
from diary.models import MdiaryBoard
from django.contrib import messages
import smtplib
import random
import string
from email.mime.text import MIMEText

# 전역 변수로 인증 코드와 이메일을 저장
verification_code = None
user_email = None

# 램덤 인증 코드 생성
def generate_verification_code():
  """랜덤 인증 코드를 생성하는 함수"""
  return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

# 이메일 인증코드
def send_verification_email(email, code):
  """이메일로 인증 코드를 보내는 함수"""
  smtpName = "smtp.naver.com"
  smtpPort = 587
  sendEmail = "wonwow55@naver.com"
  pw = "j951852753"  # 비밀번호는 실제로 안전한 방법으로 관리해야 합니다.
  title = "이메일 인증 코드"
  content = f"인증 코드: {code}"

  msg = MIMEText(content)
  msg['Subject'] = title
  msg['From'] = sendEmail
  msg['To'] = email

  try:
    s = smtplib.SMTP(smtpName, smtpPort)
    s.starttls()  # TLS 연결 설정
    s.login(sendEmail, pw)  # 로그인
    s.sendmail(sendEmail, email, msg.as_string())  # 이메일 보내기
    s.quit()  # 세션 종료
    print("메일을 발송했습니다.")
  except Exception as e:
    print("메일 발송 중 오류 발생: ", e)




# 회원가입페이지4
def join04(request):
  return render(request,'join04.html')

# 회원가입페이지3
def join03(request,id,pw,mail):
  if request.method == "POST":
    # `context`에서 전달된 데이터 가져오기
    id = request.POST.get('id')
    pw = request.POST.get('pw')  # 비밀번호는 암호화 필요
    mail = request.POST.get('full_mail')
    qs = Member.objects.create(
      id=id,
      pw=pw,  # 암호화 필요
      mail=mail,
      name=request.POST.get('name'),
      birthday=request.POST.get('date'),
      gender=request.POST.get('gender'),
    )
    
    Img.objects.create(
      id=id
    )
    
    # 회원가입시 자동으로 개인 다이어리 생성
    MdiaryBoard.objects.create(id=qs)   
     
    return redirect('loginpage:join04')  # 성공 페이지로 이동
  else:
    print('join03 확인 : ',id,pw,mail)
    context = {       
      'id': id,
      'pw': pw,
      'full_mail' : mail
    }
    return render(request,'join03.html',context)

# 회원가입페이지2
def join02(request):
  if request.method == "POST":
    # 이메일 결합
    em1 = request.POST.get('em1')  # 이메일 첫 번째 부분
    em2 = request.POST.get('em2')  # 이메일 두 번째 부분
    full_mail = f"{em1}@{em2}"  # 전체 이메일 
    print("정보1",request.POST.get('id'),request.POST.get('pw'),full_mail)
    # return render(request,'join03.html',context)  # Step 2로 이동
    id = request.POST.get('id')
    if Member.objects.filter(id=id).exists():
      messages.error(request, '이미 존재하는 아이디입니다. 다른 아이디를 입력하세요.')
      return render(request,'join02.html')
    return redirect('loginpage:join03',request.POST.get('id'),request.POST.get('pw'),full_mail)  # Step 2로 이동
  else:
    return render(request,'join02.html')
  

# 회원가입페이지1-4
def join01_4(request):
  return render(request,'join01_4.html')

# 회원가입페이지1-3
def join01_3(request):
  return render(request,'join01_3.html')

# 회원가입페이지1-2
def join01_2(request):
  return render(request,'join01_2.html')

# 회원가입페이지1-1
def join01_1(request):
  return render(request,'join01_1.html')

# 회원가입페이지1
def join01(request):
  return render(request,'join01.html')

# 비밀번호찾기3
def pw3(request,user_id):
  if request.method == "POST":

    # 비밀번호 변경
    pw = request.POST.get('password')
    qs = Member.objects.get(id=user_id)
    qs.pw = pw
    qs.save()

    # 비밀번호 변경 후 로그인 처리
    return redirect('loginpage:login')  # 비밀번호 변경 후 로그인 페이지로 리다이렉트
  else:
    return render(request,'pw3.html')

# 비밀번호찾기2
def pw2(request,user_id):
  if request.method == 'POST':
    # 입력된 데이터 유지하기 위한 기본 context 생성
    context = {
      'name': request.POST.get('name', ''),
      'birthday': request.POST.get('birthday', ''),
      'email': request.POST.get('email', ''),
      'em2': request.POST.get('em2', 'naver.com'),  # 기본 도메인
    }

    # 이메일 인증코드 발송 버튼 클릭 처리
    if 'email' in request.POST:
      # 이메일 주소 조합 및 세션 저장
      em1 = request.POST.get('email')
      em2 = request.POST.get('em2')
      full_mail = f"{em1}@{em2}"
      request.session['user_email'] = full_mail  # 세션 저장
      verification_code = generate_verification_code()
      request.session['verification_code'] = verification_code  # 인증코드 세션 저장

      # 이메일 발송
      send_verification_email(full_mail, verification_code)

      # 회원 정보 확인
      if not Member.objects.filter(name=context['name'], birthday=context['birthday']).exists():
        messages.error(request, '이름과 생년월일이 일치하지 않습니다.')
        return render(request, 'pw2.html', context)

      messages.success(request, '인증 코드가 이메일로 발송되었습니다. 확인해주세요.')
      return render(request, 'pw2.html', context)

    # 인증코드 확인 버튼 클릭 처리
    elif 'verification_code' in request.POST:
      entered_code = request.POST.get('verification_code')
      saved_code = request.session.get('verification_code')
      user_email = request.session.get('user_email')

      # 이름, 생년월일, 이메일 확인
      if not Member.objects.filter(name=context['name'], birthday=context['birthday']).exists():
        messages.error(request, '입력된 정보가 일치하지 않습니다. 다시 확인해주세요.')
        return render(request, 'pw2.html', context)

      # 인증 코드 확인
      if entered_code != saved_code:
        messages.error(request, '잘못된 인증 코드입니다.')
        return render(request, 'pw2.html', context)

      # 인증 성공 시 리다이렉트
      return redirect('/loginpage/pw3/'+user_id)

  # GET 요청 처리 (빈 입력 폼 렌더링)
  return render(request, 'pw2.html', {
      'name': '',
      'birthday': '',
      'email': '',
      'em2': 'naver.com',
  })

# 비밀번호찾기1
def pw(request):
  if request.method == "POST":
    # 아이디 확인
    user_id = request.POST.get('id')
    if not Member.objects.filter(id=user_id).exists():
      messages.error(request, '아이디를 확인해 주세요.')
      return render(request, 'pw.html')
    else:
      request.session['user_id'] = user_id
      return redirect('/loginpage/pw2/'+user_id)
  else:
    return render(request,'pw.html')

# 아이디찾기2
def id2(request,user_id):
  return render(request,'id2.html', {'user_id': user_id})


# 아이디찾기1
def id(request):
  if request.method == 'POST':
    # 입력된 데이터 유지하기 위한 기본 context 생성
    context = {
        'name': request.POST.get('name', ''),
        'birthday': request.POST.get('birthday', ''),
        'email': request.POST.get('email', ''),
        'em2': request.POST.get('em2', 'naver.com'),  # 기본 도메인
    }

    # 이메일 인증코드 발송 버튼 클릭 처리
    if 'email' in request.POST:
      # 이메일 주소 조합 및 세션 저장
      em1 = request.POST.get('email')
      em2 = request.POST.get('em2')
      full_mail = f"{em1}@{em2}"
      request.session['user_email'] = full_mail  # 세션 저장
      verification_code = generate_verification_code()
      request.session['verification_code'] = verification_code  # 인증코드 세션 저장

      # 이메일 발송
      send_verification_email(full_mail, verification_code)

      # 회원 정보 확인
      if not Member.objects.filter(name=context['name'], birthday=context['birthday']).exists():
        messages.error(request, '이름과 생년월일이 일치하지 않습니다.')
        return render(request, 'id.html', context)

      messages.success(request, '인증 코드가 이메일로 발송되었습니다. 확인해주세요.')
      return render(request, 'id.html', context)

    # 인증코드 확인 버튼 클릭 처리
    elif 'verification_code' in request.POST:
      entered_code = request.POST.get('verification_code')
      saved_code = request.session.get('verification_code')
      user_email = request.session.get('user_email')

      # 이름, 생년월일, 이메일 확인
      if not Member.objects.filter(name=context['name'], birthday=context['birthday']).exists():
        messages.error(request, '입력된 정보가 일치하지 않습니다. 다시 확인해주세요.')
        return render(request, 'id.html', context)

      # 인증 코드 확인
      if entered_code != saved_code:
        messages.error(request, '잘못된 인증 코드입니다.')
        return render(request, 'id.html', context)

      # 인증 성공 시 리다이렉트
      user = Member.objects.get(name=context['name'], birthday=context['birthday'])
      return redirect('loginpage:id2', user_id=user.id)
    # GET 요청 처리 (빈 입력 폼 렌더링)
  return render(request, 'id.html', {
      'name': '',
      'birthday': '',
      'email': '',
      'em2': 'naver.com',
  })


# 로그인페이지
def login(request):
  if request.method == "POST":
    id = request.POST.get('id')
    pw = request.POST.get('pw')
    qs = Member.objects.filter(id=id, pw=pw)
    if qs.exists():  # 로그인 성공
      mail = qs[0].mail
      name = qs[0].name
      request.session['session_id'] = id
      request.session['session_mail'] = mail
      request.session['session_name'] = name
      print("2")
      return redirect('/index')  # 성공 시 리다이렉트
    else:  # 로그인 실패
      print("3")
      context = {'lmsg': "아이디와 비밀번호를 확인해 주세요."}
      return render(request, 'login.html', context)  # 실패 시 에러 메시지와 함께 템플릿 렌더링
  else:
    print("1")
    return render(request, 'login.html')
  