from django.shortcuts import render
from customer.models import NoticeBoard
from loginpage.models import Member
from mypage.models import Img

# Create your views here.
def main(request):
  if request.method == 'GET':
    # 프로필 가져오기 
    mem = Member.objects.filter(id = request.session['session_id'])
    qb = Img.objects.filter(id=request.session['session_id']).first()
    qs = NoticeBoard.objects.filter(category=1, status='게시중').order_by('-bno')[:5]
    qs_post = NoticeBoard.objects.filter(category=2, status='게시중').order_by('-bno')
    context = {'notice_5':qs, 'mem_info':mem[0], 'post_lists':qs_post, 'qb':qb}

  # 1:1 문의 작성하기 버튼 눌렀을 때
  else:
    mem = Member.objects.filter(id = request.session['session_id'])
    requ_title = request.POST.get('requ_title')
    requ_content = request.POST.get('requ_content')
    request_file = request.FILES.get('request_file')
    requ_mail = request.POST.get('requ_mail')
    NoticeBoard.objects.create(userid=mem[0].id, btitle=requ_title, bcontent=requ_content, bfile=request_file, bmail=requ_mail, category=3, status='답변 전')
    
    qb = Img.objects.filter(id=request.session['session_id']).first()
    qs = NoticeBoard.objects.filter(category=1, status='게시중').order_by('-bno')[:5]
    qs_post = NoticeBoard.objects.filter(category=2).order_by('-bno')
    context = {'qmsg':1,'notice_5':qs, 'mem_info':mem[0], 'post_lists':qs_post, 'qb':qb}
  return render(request, 'customer_service.html', context)

def noticelist(request):
  # 프로필 가져오기 
  mem = Member.objects.filter(id = request.session['session_id'])
  qb = Img.objects.filter(id=request.session['session_id']).first()
  qs = NoticeBoard.objects.filter(category=1, status='게시중').order_by('-bno')
  context = {'notice_list':qs, 'mem_info':mem[0], 'qb':qb,}
  return render(request, 'customer_notice_list.html', context)

def noticeview(request, bno):
  # 프로필 가져오기 
  mem = Member.objects.filter(id = request.session['session_id'])
  qb = Img.objects.filter(id=request.session['session_id']).first()
  qs = NoticeBoard.objects.get(bno=bno)
  context = {'view':qs, 'mem_info':mem[0], 'qb':qb,}
  return render(request, 'customer_notice_view.html', context)