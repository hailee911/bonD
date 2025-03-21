from django.shortcuts import render,redirect
from admin1.models import Administrator
from loginpage.models import Member
from loginpage.models import Member
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from loginpage.models import Member
from django.db.models import Max
from admin1.models import Administrator
from customer.models import NoticeBoard


# 어드민 로그인
def admin_login(request):
	if request.method == 'GET':
		return render(request, 'admin_login.html')
	else:
		id = request.POST.get('user_id')
		pw = request.POST.get('user_pw')

		qs = Administrator.objects.filter(id=id,pw=pw)
		if qs:
			request.session['session_id'] = id
			request.session['session_role'] = qs[0].role

			context = {'lmsg':'1'}
		else:
			context = {'lmsg':'0'}
		return render(request, 'admin_login.html', context)
	

# 어드민 로그아웃
def admin_logout(request):
	request.session.clear()
	context = {"outMsg":'1'}
	return render(request, 'admin_memList.html', context)
	

# 유저 리스트
def admin_memList(request):
	qs = Member.objects.all()
	context = {"mlist":qs}
	return render(request, 'admin_memList.html', context)

# 유저 상세정보
def admin_memView(request,id):
	qs = Member.objects.get(id=id)
	context = {"mem":qs}
	return render(request, 'admin_memView.html', context)

# 유저 정보 수정
def admin_memUpdate(request,id):
	if request.method == "GET":
		qs = Member.objects.get(id=id)
		context = {"mem":qs}
		return render(request, 'admin_memUpdate.html', context)
	else:
		id = request.POST.get('user_id')
		name = request.POST.get('user_name')
		nicName = request.POST.get('nickname')
		mail = request.POST.get('email')
		mdate = request.POST.get('sdate')

		qs = Member.objects.get(id=id)
		qs.id = id
		qs.name = name
		qs.nicName = nicName
		qs.mail = mail
		qs.mdate = mdate
		qs.save()
		return redirect('admin1:admin_memView', id)

# 유저정보 삭제
def admin_memDelete(request,id):
	Member.objects.get(id=id).delete()

	context = {'dmsg':id}
	return render(request, 'admin_memView.html', context)

# 체크박스 유저 삭제
def admin_memsDelete(request):
	if request.method == 'POST':
			try:
					data = json.loads(request.body)  # 요청에서 JSON 데이터 파싱
					members_to_delete = data.get('members', [])

					# 실제로 데이터베이스에서 삭제
					for member_id in members_to_delete:
							# Member는 회원 테이블 모델로 변경해야 합니다.
							Member.objects.filter(id=member_id).delete()

					return JsonResponse({'status': 'success'}, status=200)
			except Exception as e:
					return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
	return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

# 유저추가페이지
def admin_memAdd(request):
	if request.method == 'GET':
		return render(request, 'admin_memAdd.html')
	else:
		id = request.POST.get('user_id')
		name = request.POST.get('user_name')
		nicName = request.POST.get('nickname')
		mail = request.POST.get('email')
		birthday = request.POST.get('birthday')
		gender = request.POST.get('gender')
		mdate = request.POST.get('sdate')

		qs = Member.objects.create(id=id,name = name,nicName = nicName,mail = mail,birthday = birthday,gender = gender,mdate = mdate)
	
		qs.save()

		context = {"amsg":name}
		return render(request, 'admin_memList.html', context)


# 관리자 리스트
def admin_adminList(request):
	qs = Administrator.objects.all()
	context = {"adminList":qs}
	return render(request, 'admin_adminList.html', context)

# 관리자 추가
def admin_adminAdd(request):
	if request.method == 'GET':
		return render(request, 'admin_adminAdd.html')
	else:
		id = request.POST.get('admin_id')
		pw = request.POST.get('admin_pw')
		name = request.POST.get('admin_name')
		tel = request.POST.get('tel')
		role = request.POST.get('role')
		if role == '3':
			nickname = '수퍼관리자'
		else:
			nickname = '관리자'

		qs = Administrator.objects.create(id=id,pw=pw,name=name,nickname=nickname,tel=tel,role=role)
		no = Administrator.objects.aggregate(max_ano = Max('ano'))
		qs.ano = no['max_ano']+1
		qs.save()
		
		return redirect('/admin1/admin_adminList/')

# 관리자 상세보기
def admin_adminView(request,id):
	qs = Administrator.objects.get(id=id)
	context = {"admin":qs}
	return render(request, 'admin_adminView.html', context)

# 관리자 정보수정
def admin_adminUpdate(request,id):
	if request.method == 'GET':
		qs = Administrator.objects.get(id=id)
		context = {"admin":qs}
		return render(request, 'admin_adminUpdate.html', context)
	else:
		id = request.POST.get('admin_id')
		pw = request.POST.get('admin_pw')
		name = request.POST.get('admin_name')
		tel = request.POST.get('tel')
		role = request.POST.get('role')
		if role == '3':
			nickname = '수퍼관리자'
		else:
			nickname = '관리자'

		qs = Administrator.objects.get(id=id)
		qs.id = id
		qs.pw = pw
		qs.name = name
		qs.tel = tel
		qs.role = role
		qs.nickname = nickname
		qs.save()
		return redirect('admin1:admin_adminView', id)
	
# 관리자 삭제
def admin_adminDelete(request,id):
	Administrator.objects.get(id=id).delete()

	context = {'dmsg':id}
	return render(request, 'admin_adminView.html', context)


# 체크박스 관리자 삭제
def admin_adminsDelete(request):
	if request.method == 'POST':
			try:
					data = json.loads(request.body)  # 요청에서 JSON 데이터 파싱
					members_to_delete = data.get('members', [])
					# print("Members to delete:", members_to_delete)

					# 실제로 데이터베이스에서 삭제
					for member_id in members_to_delete:
							Administrator.objects.filter(id=member_id).delete()

					return JsonResponse({'status': 'success'}, status=200)
			except Exception as e:
					return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
	return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


# 공지사항 리스트
def admin_noticeList(request):
	qs = NoticeBoard.objects.filter(category=1).order_by("-bno")
	context = {"notiList":qs}
	return render(request, 'admin_noticeList.html', context)

def admin_noticeList2(request):
	# 요청에서 데이터 가져오기
	data = json.loads(request.body)
	status = data.get('status')
	bno = data.get('bno')
	print(status)
	print(bno)

	# bno로 객체 조회 및 상태 업데이트
	qs = NoticeBoard.objects.get(bno=bno)
	qs.status = status
	qs.save()

	return JsonResponse({'success': True})

# 공지사항 쓰기
def admin_notiWrite(request):
	if request.method == 'GET':
		return render(request, 'admin_notiWrite.html')
	else:
		id = request.session.get('session_id')
		member = Administrator.objects.get(id=id)
		btitle = request.POST.get("title")
		bcontent = request.POST.get("content")
		bfile = request.FILES.get('bfile','')
		category = 1
		NoticeBoard.objects.create(member=member,btitle=btitle,bcontent=bcontent,bfile=bfile,category=category, status='게시안함')
		context = {'wmsg':'1'}
		return render(request, 'admin_noticeList.html', context)
	
# 공지사항 상세보기
def admin_notiView(request, bno):
	qs = NoticeBoard.objects.get(bno=bno)
	## 이전글
	prev_qs = NoticeBoard.objects.filter(bno__lt=bno, category=1).order_by('-bno').first()
	# 다음글
	next_qs = NoticeBoard.objects.filter(bno__gt=bno, category=1).order_by('bno').first()
	
	context = {
		"noti": qs,
		"prev_board": prev_qs,
		"next_board": next_qs,
	}
	return render(request, 'admin_notiView.html', context)

# 공지사항 삭제
def admin_notiDelete(request, bno):
	NoticeBoard.objects.get(bno=bno).delete()
	context = {'dmsg':bno}
	return render(request, 'admin_noticeList.html', context)

# 체크박스 게시글 삭제
def admin_notisDelete(request):
	if request.method == 'POST':
			try:
					data = json.loads(request.body)  # 요청에서 JSON 데이터 파싱
					members_to_delete = data.get('members', [])
					# print("Members to delete:", members_to_delete)

					# 실제로 데이터베이스에서 삭제
					for member_id in members_to_delete:
							NoticeBoard.objects.filter(bno=member_id).delete()

					return JsonResponse({'status': 'success'}, status=200)
			except Exception as e:
					return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
	return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

# 포스트 리스트
def admin_postList(request):
	qs = NoticeBoard.objects.filter(category=2).order_by("-bno")
	context = {"postList":qs}
	return render(request, 'admin_postList.html', context)

def admin_postList2(request):
	# 요청에서 데이터 가져오기
	data = json.loads(request.body)
	status = data.get('status')
	bno = data.get('bno')

	# bno로 객체 조회 및 상태 업데이트
	qs = NoticeBoard.objects.get(bno=bno)
	qs.status = status
	qs.save()

	return JsonResponse({'success': True})


# 포스트 쓰기
def admin_postWrite(request):
	if request.method == 'GET':
		return render(request, 'admin_postWrite.html')
	else:
		id = request.session.get('session_id')
		member = Administrator.objects.get(id=id)
		btitle = request.POST.get("title")
		bcontent = request.POST.get("content")
		bfile = request.FILES.get('bfile','')
		bfile_thumbnail = request.FILES.get('bfile_thumbnail','')
		category = 2
		NoticeBoard.objects.create(member=member,btitle=btitle,bcontent=bcontent,bfile_thumbnail=bfile_thumbnail,bfile=bfile,category=category, status='게시안함')
		context = {'wmsg':'1'}
		return render(request, 'admin_postList.html', context)

# 포스트 상세보기
def admin_postView(request, bno):
	qs = NoticeBoard.objects.get(bno=bno)
	## 이전글
	prev_qs = NoticeBoard.objects.filter(bno__lt=bno, category=2).order_by('-bno').first()
	# 다음글
	next_qs = NoticeBoard.objects.filter(bno__gt=bno, category=2).order_by('bno').first()
	
	context = {
		"post": qs,
		"prev_board": prev_qs,
		"next_board": next_qs,
	}
	return render(request, 'admin_postView.html', context)

# 포스트 삭제
def admin_postDelete(request, bno):
	NoticeBoard.objects.get(bno=bno).delete()
	context = {'dmsg':bno}
	return render(request, 'admin_postList.html', context)


# 1:1 리스트
def admin_qList(request):
	qs_ok = NoticeBoard.objects.filter(category=3, status='답변 완료').order_by("-bno")
	qs_no = NoticeBoard.objects.filter(category=3, status='답변 전').order_by("-bno")
	# 작성자
	context = {'oklist':qs_ok, 'nolist':qs_no}
	return render(request, 'admin_qList.html', context)

def admin_qListView(request, bno):
	qs = NoticeBoard.objects.get(bno=bno)
	## 이전글
	prev_qs = NoticeBoard.objects.filter(bno__lt=bno, category=3).order_by('-bno').first()
	# 다음글
	next_qs = NoticeBoard.objects.filter(bno__gt=bno, category=3).order_by('bno').first()
	
	context = {
		"q": qs,
		"prev_board": prev_qs,
		"next_board": next_qs,
	}

	return render(request, 'admin_qListView.html', context)

def admin_qListchg(request, bno):
	qs = NoticeBoard.objects.get(bno=bno)
	qs.status = '답변 완료'
	qs.save()
	return redirect('/admin1/admin_qList/')

def admin_qListchg2(request):
	import json
	data = json.loads(request.body)
	members = data.get('members', [])  # members 배열 받기


	# 'bno'에 해당하는 항목들을 찾아 'status'를 '답변 완료'로 업데이트
	NoticeBoard.objects.filter(bno__in=members).update(status="답변 완료")

	return render(request, 'admin_qList.html')

def admin_qListchg3(request):
	import json
	data = json.loads(request.body)
	members = data.get('members', [])  # members 배열 받기


	# 'bno'에 해당하는 항목들을 찾아 'status'를 '답변 완료'로 업데이트
	NoticeBoard.objects.filter(bno__in=members).update(status="답변 전")

	return render(request, 'admin_qList.html')

