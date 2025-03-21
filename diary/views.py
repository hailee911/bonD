from django.shortcuts import render, redirect
from loginpage.models import Member
from diary.models import Letter
from django.utils import timezone
from diary.models import Content
from diary.models import GroupDiary
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Max
from django.db.models import Q
from comment.models import Comment  # 댓글 모델 가져오기
from mypage.models import Img       # 프로필 사진 가져오기
from notifications.utils import create_notification
from django.views.decorators.cache import cache_control
from django.http import JsonResponse, HttpResponseForbidden
from like.models import Like


# 우체통
from .models import MdiaryBoard

## 다이어리 HOME
def diaryHome(request):
	id = request.session.get('session_id')
	name = request.session.get('session_name')
	my_info = Member.objects.filter(id=id).first()
	qs_group = GroupDiary.objects.filter(member=id)

	## 공유 일기장
	# 1. 유저가 생성공유일기장

	qs_createdDiary = GroupDiary.objects.filter(Q(member__id=id) & Q(role=1))
	c_context = {} #변수

	if qs_createdDiary:
		# 초대멤버가져오기
		qs_joinedMem = GroupDiary.objects.filter(gno=qs_createdDiary[0].gno, role=2)
		if qs_joinedMem:
			c_context = {"creator":qs_createdDiary[0], "user_name":name, "joined_members":qs_joinedMem}
		else:
			c_context = {"creator":qs_createdDiary[0], "user_name":name,}
	

	# 2. 유저가 가입한 공유일기장
	qs_joinedDiary = GroupDiary.objects.filter(Q(member__id=id) & Q(role=2))
	if qs_joinedDiary:
		# 멤버 정보가져오기
		# 방장
		gno = qs_joinedDiary[0].gno
		qs_joinedMem = GroupDiary.objects.filter(gno=qs_joinedDiary[0].gno, role=2)
		qs_cMem = Member.objects.filter(created_group__gno=gno).first()

		jmems = []
		for jmem in qs_joinedMem:
			member = jmem.member
			j = Member.objects.get(id=member.id)
			jmems.append(j.name)
		c_context['cMem'] = qs_cMem
		c_context['join_d'] = list(qs_joinedMem)
		c_context['joined_names'] = jmems


	## 개인 다이어리
	qs_pDiary = MdiaryBoard.objects.get(id=id)
	c_context['pDiary'] = qs_pDiary

	c_context['qb'] = Img.objects.filter(id=id).first()
	c_context['info'] = my_info
	c_context['group'] = qs_group
	return render(request,'diaryHome.html',c_context)


	# 우체통
	qs = Letter.objects.all().order_by("ldate")
	member = Member.objects.filter(id=id)
	# personal_diaries = MdiaryBoard.objects.select_related('id').all() # 개인 다이어리 데이터 가져오기
	if member:
		user_nic = member[0].nicName
		context = {"list":qs ,'user_nic':user_nic}
		return render(request,'diaryHome.html',context)
	else:
		context = {'list':qs}
		return render(request,'diaryHome.html',context)
	
		


## 가족다이어리 생성
def diaryMake(request):
	if request.method == 'GET':
		qs_Member = Member.objects.all()
		id = request.session['session_id']
		my_info = Member.objects.filter(id=id).first()
		qb = Img.objects.filter(id=id).first()
		qs_createdDiary = GroupDiary.objects.filter(Q(member__id=id) & Q(role=1))
		if qs_createdDiary:
			context = {"gmsg":"0", 'info':my_info, 'qb':qb}
			return render(request,'diaryHome.html', context)
		else:
			context = {'members':qs_Member,"gmsg":"1", 'info':my_info, 'qb':qb}
			return render(request,'diaryMake.html', context)

	else:

		id = request.session['session_id']
		member = Member.objects.get(id=id)
		gtitle = request.POST.get('gtitle')
		gName = request.POST.get('gName')
		created_at = request.POST.get('created_at','')
		search_members = request.POST.getlist('search_members[]')
		
		# GroupDiary에 방장 저장
		qs_creator = GroupDiary.objects.create(gtitle=gtitle, gName=gName, created_at=created_at, member=member)
		no = GroupDiary.objects.aggregate(max_gno = Max('gno'))
		qs_creator.gno = no['max_gno']+1
		qs_creator.role = 1
		qs_creator.save()
		
		# Member에 created_group에 방장 저장
		qs_cMem = Member.objects.get(id=id)
		qs_cMem.created_group = qs_creator
		qs_cMem.save()

		# 초대 멤버 저장
		for sMem in search_members:
			# GroupDiary에 멤버 저장
			gno = qs_creator.gno
			role = 2
			qs_sMem = Member.objects.get(id=sMem)
			qs_joinedMem = GroupDiary.objects.create(gno=gno, gtitle=gtitle, gName=gName, created_at=created_at, member=qs_sMem, role=role)

			# Member에 joined_group에 멤버 저장
			qs_sMem.joined_group = qs_joinedMem
			qs_sMem.save()
		
		context = {"gmsg":"1"}

		return render(request, 'diaryHome.html', context)
		

## 내 다이어리 목록
def MdiaryList(request):
	# 세션에 저장된 ID 가져오기
	session_id = request.session.get('session_id')  # 세션에서 'session_id'를 가져옴

	# 세션에 해당하는 ID가 존재하는지 확인
	if not session_id:
			return render(request, 'error.html', {'message': '세션 ID가 존재하지 않습니다.'})
	
	# session_id를 기준으로 Member 찾기
	member = Member.objects.filter(id=session_id).first()
	
	# member가 없으면 에러 처리
	if not member:
			return render(request, 'error.html', {'message': '사용자 정보가 존재하지 않습니다.'})

	# MdiaryBoard와 Content 가져오기
	mdiary = MdiaryBoard.objects.filter(id=member).first()  # 사용자와 연결된 MdiaryBoard
	if not mdiary:
		return render(request, 'error.html', {'message': '다이어리 정보가 없습니다.'})

	# 해당 멤버의 Content 가져오기
	qs = Content.objects.filter(member=member).select_related('mdiary').order_by("-cdate")
	qb = Img.objects.filter(id=session_id).first()
	npage = request.GET.get('npage', 1)
	paginator = Paginator(qs, 10)
	page_obj = paginator.get_page(npage)
	
	context = {'content': page_obj.object_list,
						'MdiaryList':page_obj,
						'mdiary':mdiary,
						'qb':qb,
						'info':member,}
	return render(request, 'MdiaryList.html', context)
		
	
# 개인 다이어리 제목 수정
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

def update_diary_title(request):
		if request.method == 'POST' and request.is_ajax():
				new_title = request.POST.get('title')
				mdiary = get_object_or_404(MdiaryBoard, id=request.user.id)  # 로그인된 사용자에 맞는 다이어리 가져오기
				mdiary.mtitle = new_title
				mdiary.save()
				return JsonResponse({'success': True})
		return JsonResponse({'success': False})


						

# 다이어리 작성 저장
def diaryWrite(request):
		if request.method == "GET":
				# 세션에서 사용자 ID 가져오기
				id = request.session.get('session_id')  # 현재 사용자의 ID 가져오기
				my_info = Member.objects.filter(id=id).first()
				qb = Img.objects.filter(id=id).first()
				current_date = timezone.now().date().strftime('%Y-%m-%d')
				# 생성한 그룹과 참여한 그룹 가져오기
				user = Member.objects.filter(id=id)
				created_group = user[0].created_group
				joined_group = user[0].joined_group
				return render(request, 'diaryWrite.html', {
						'current_date': current_date,
						'created_group': created_group,
						'joined_group': joined_group,
						'info':my_info,
						'qb':qb,
				})
		elif request.method == "POST":
				current_date = timezone.now().date().strftime('%Y-%m-%d')
				# 세션에서 사용자 ID 가져오기
				id = request.session.get('session_id')  # 세션에서 사용자 ID 가져오기
				if not id:
						return HttpResponse("로그인 정보가 없습니다.", status=400)
				# Member 모델에서 해당 ID로 회원 조회
				member = Member.objects.filter(id=id).first()  # 없으면 None 반환
				if not member:
						return HttpResponse("사용자 정보가 존재하지 않습니다.", status=400)
				# 다이어리 작성 내용 저장
				title = request.POST.get('title')
				content = request.POST.get('content')
				image = request.FILES.get('image')
				diary_idc = request.POST.get('diary_idc','')
				diary_idj = request.POST.get('diary_idj','')
				selected_groups = [diary_idc,diary_idj]
				date = request.POST.get('date')
				if date != current_date:
					cdate = date
				else:
					cdate = timezone.now()
				
				# Content 객체 생성하여 저장
				new_diary = Content(
						member=member,
						ctitle=title,
						ccontent=content,
						image=image,
						cdate=cdate,
				)
				new_diary.save()
				## 공유하려는 다이어리가 있으면
				if selected_groups[0] == '' and selected_groups[1] == '':
						return redirect('diary:MdiaryList')
				else:
						# join된 일기장에만 공유
						if selected_groups[0] == '':
								joined_group = GroupDiary.objects.filter(gno=selected_groups[1]).first()
								print("!!!!`12`12`1",joined_group)
								print("!!!!!!!!!!!!!1",joined_group.gno)
								if joined_group:  # joined_group이 None이 아닌 경우에만 추가
										new_diary.group_diary.add(joined_group)
										# 알림 생성
										for member in GroupDiary.objects.filter(gno=joined_group.gno).exclude(member__id=id):
												create_notification(
														user_id=member.member.id,
														message=f"{new_diary.member.name}님의 새로운 기록이 공유되었습니다!"
												)

						# create 한 일기장에만 공유
						elif selected_groups[1] == '':
								created_group = GroupDiary.objects.filter(gno=selected_groups[0]).first()
								if created_group:
										new_diary.group_diary.add(created_group)
										# 알림 생성
										for member in GroupDiary.objects.filter(gno=created_group.gno).exclude(member__id=id):
												create_notification(
														user_id=member.member.id,
														message=f"{new_diary.member.name}님의 새로운 기록이 공유되었습니다!"
												)

						# 모두 공유
						else:
								created_group = GroupDiary.objects.filter(gno=selected_groups[0]).first()
								joined_group = GroupDiary.objects.filter(gno=selected_groups[1]).first()
								if created_group:
										new_diary.group_diary.add(created_group)
										# 알림 생성
										for member in GroupDiary.objects.filter(gno=created_group.gno).exclude(member__id=id):
												create_notification(
														user_id=member.member.id,
														message=f"{new_diary.member.name}님의 새로운 기록이 공유되었습니다!"
												)
								if joined_group:
										new_diary.group_diary.add(joined_group)
										# 알림 생성
										for member in GroupDiary.objects.filter(gno=joined_group.gno).exclude(member__id=id):
												create_notification(
														user_id=member.member.id,
														message=f"{new_diary.member.name}님의 새로운 기록이 공유되었습니다!"
												)

						return redirect('diary:MdiaryList')  # 다이어리 리스트로 리다이렉트

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def diary_view(request,cno):
		# mdiary = Content.objects.filter(cno=cno)
		session_id = request.session.get('session_id')
		member = Member.objects.filter(id=session_id).first()
		mdiary = MdiaryBoard.objects.filter(id=member).first()
		qb = Img.objects.filter(id=session_id).first()
		current_post = Content.objects.filter(cno=cno)
		if not current_post:
				return HttpResponse("게시물이 존재하지 않습니다.", status=404)

		# 현재 게시글 정보 가져오기
		current_diary = current_post.first()

		# 이전 글 (현재 게시글 날짜보다 작은 가장 가까운 글)
		previous_post = (
				Content.objects.filter(member=session_id, cdate__lt=current_diary.cdate)
				.order_by('-cdate')
				.first()
		)

		# 다음 글 (현재 게시글 날짜보다 큰 가장 가까운 글)
		next_post = (
				Content.objects.filter(member=session_id, cdate__gt=current_diary.cdate)
				.order_by('cdate')
				.first()
		)

		# 현재 페이지 번호 가져오기
		pageNum = int(request.GET.get('pageNum', 1))

		# 현재 경로가 /diary/MdiaryList/인지 확인
		referer = request.META.get('HTTP_REFERER', '')
		is_mdiary_list = referer.endswith('/diary/MdiaryList/')

		# 댓글을 불러올 때, 댓글에 설정된 group_num을 기준으로 필터링
		comments = Comment.objects.filter(content=current_post[0]).order_by('-created_at')

		# 사용자가 볼 수 있는 댓글만 필터링
		visible_comments = []
		for comment in comments:
			qb1 = Img.objects.filter(id=comment.member.id).first()
			visible_comments.append((comment, qb1.img))
			
	
		# 좋아요 상태 확인
		user_liked = False
		like_count = 0
		if member:
				like_obj = Like.objects.filter(content=current_post.first(), member=member).first()
				if like_obj:
						user_liked = True
				
				like_count = Like.objects.filter(content=current_post.first()).count()

		context = {
				'cont': current_post[0],
				'previous_post': previous_post,  # 이전글 1개
				'next_post': next_post,          # 다음글 1개
				'pageNum': pageNum,
				'mdiary':mdiary,
				'diary':'Mdiary',
				'is_mdiary_list': is_mdiary_list,  # 템플릿에서 사용 가능
				'qb':qb,                            # 프사
				'member':member,                           # 내정보
				'comments': visible_comments,             # 댓글 리스트
				'comment_success': request.GET.get('comment_success', False),  # 댓글 등록 성공 여부
        'like_count': like_count,
				'user_liked': user_liked,
		}
		return render(request,'diary_view.html',context)


## 가족다이어리 view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Cdiary_view(request,cno):
		# mdiary = Content.objects.filter(cno=cno)
		session_id = request.session.get('session_id')
		member = Member.objects.filter(id=session_id).first()
		Cdiary = GroupDiary.objects.filter(member=member).first()
		qb = Img.objects.filter(id=session_id).first()
		current_post = Content.objects.filter(cno=cno)
		if not current_post:
				return HttpResponse("게시물이 존재하지 않습니다.", status=404)

			# 현재 게시글 정보 가져오기
		current_diary = Content.objects.get(cno=cno)

		# 현재 그룹 다이어리 가져오기
		current_Cdiaryname = member.created_group
		current_gno = current_Cdiaryname.gno

		# 그 그룹의 일기 가져오기
		joingroup = GroupDiary.objects.filter(gno=current_gno).first()
		# join다이어리의 Content 가져오기
		contents = joingroup.content_set.all().order_by("-cdate")  # 해당 GroupDiary에 연결된 모든 Content 객체 가져오기


		# 이전 글 (현재 게시글 날짜보다 작은 가장 가까운 글)
		# previous_post = next((post for post in contents if post.cdate < current_diary.cdate), None)
		previous_post = contents.filter(cdate__lt=current_diary.cdate).order_by('-cdate').first()
		next_post = contents.filter(cdate__gt=current_diary.cdate).order_by('cdate').first()
		

		# 현재 페이지 번호 가져오기
		pageNum = int(request.GET.get('pageNum', 1))

		# 댓글을 불러올 때, 댓글에 설정된 group_num을 기준으로 필터링
		comments = Comment.objects.filter(content=current_post[0]).order_by('-created_at')

		# 사용자가 볼 수 있는 댓글만 필터링
		visible_comments = []
		for comment in comments:
				# 사용자가 댓글을 볼 수 있는 조건
				if comment.group_num == member.created_group.gno:
						qb1 = Img.objects.filter(id=comment.member.id).first()
						visible_comments.append((comment, qb1.img))
      
    # 좋아요 상태 확인
		user_liked = False
		like_count = 0
		if member:
				like_obj = Like.objects.filter(content=current_post.first(), member=member).first()
				if like_obj:
						user_liked = True
				
				like_count = Like.objects.filter(content=current_post.first()).count()

		context = {
				'cont': current_post[0],
				'previous_post': previous_post,  # 이전글 1개
				'next_post': next_post,          # 다음글 1개
				'pageNum': pageNum,
				'mdiary':Cdiary,
				'diary':'Cdiary',
				'qb':qb,
				'member':member,
				'comments': visible_comments,             # 댓글 리스트
				'comment_success': request.GET.get('comment_success', False),  # 댓글 등록 성공 여부
        'like_count': like_count,
				'user_liked': user_liked,
		}
		return render(request,'diary_view.html',context)

## 가족다이어리 view
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def Jdiary_view(request,cno):
		# mdiary = Content.objects.filter(cno=cno)
		session_id = request.session.get('session_id')
		member = Member.objects.filter(id=session_id).first()
		Jdiary = GroupDiary.objects.filter(member=member).first()
		qb = Img.objects.filter(id=session_id).first()
		current_post = Content.objects.filter(cno=cno)
		if not current_post:
				return HttpResponse("게시물이 존재하지 않습니다.", status=404)

			# 현재 게시글 정보 가져오기
		current_diary = Content.objects.get(cno=cno)

		# 현재 그룹 다이어리 가져오기
		current_Jdiaryname = member.joined_group
		current_gno = current_Jdiaryname.gno

		# 그 그룹의 일기 가져오기
		joingroup = GroupDiary.objects.filter(gno=current_gno).first()
		# join다이어리의 Content 가져오기
		contents = joingroup.content_set.all().order_by("-cdate")  # 해당 GroupDiary에 연결된 모든 Content 객체 가져오기


		# 이전 글 (현재 게시글 날짜보다 작은 가장 가까운 글)
		previous_post = contents.filter(cdate__lt=current_diary.cdate).order_by('-cdate').first()
		next_post = contents.filter(cdate__gt=current_diary.cdate).order_by('cdate').first()
		

		# 현재 페이지 번호 가져오기
		pageNum = int(request.GET.get('pageNum', 1))

		# 댓글을 불러올 때, 댓글에 설정된 group_num을 기준으로 필터링
		comments = Comment.objects.filter(content=current_post[0]).order_by('-created_at')

		# 사용자가 볼 수 있는 댓글만 필터링
		visible_comments = []
		for comment in comments:
				# 사용자가 댓글을 볼 수 있는 조건
				if comment.group_num == member.joined_group.gno:
						qb1 = Img.objects.filter(id=comment.member.id).first()
						visible_comments.append((comment, qb1.img))
			
  # 좋아요 상태 확인
		user_liked = False
		like_count = 0
		if member:
				like_obj = Like.objects.filter(content=current_post.first(), member=member).first()
				if like_obj:
						user_liked = True
				
				like_count = Like.objects.filter(content=current_post.first()).count()

		context = {
				'cont': current_post[0],
				'previous_post': previous_post,  # 이전글 1개
				'next_post': next_post,          # 다음글 1개
				'pageNum': pageNum,
				'mdiary':Jdiary,
				'diary':'Jdiary',
				'qb':qb,
				'member':member,
				'comments': visible_comments,             # 댓글 리스트
				'comment_success': request.GET.get('comment_success', False),  # 댓글 등록 성공 여부
				'like_count': like_count,
				'user_liked': user_liked,
		}
		return render(request,'diary_view.html',context)




## 글수정페이지, 글수정 저장
def dmodify(request,cno):
	print("게시글 번호 : ",cno)
	if request.method == "GET":
		id = request.session.get('session_id')  # 현재 사용자의 ID 가져오기
		qb = Img.objects.filter(id=id).first()
		qs = Content.objects.filter(cno=cno)
		user = Member.objects.filter(id=id)
		created_group = user[0].created_group
		joined_group = user[0].joined_group
		# 내가 공유한 다이어리가 있는지 확인
		share = qs[0].group_diary.all()
		if share.exists():
			if len(share) == 2:
				created_d = 1
				joined_d = 1
			else:
				if created_group.gName == share[0].gName:
					created_d = 1
					joined_d = 0
				else:
					joined_d = 1
					created_d = 0
		else:
			created_d = 0
			joined_d = 0

		context = {"diary":qs[0],
						 "created_group":created_group,
						 "created_d":created_d,
						 "joined_group":joined_group,
						 "joined_d":joined_d,
						 'info':user,
						 'qb':qb,}
		return render(request,'dmodify.html',context)
	
	else:  #post
		# cno = request.POST.get("cno")
		ctitle = request.POST.get("title")
		ccontent = request.POST.get("content")
		cdate = request.POST.get("date")
		image = request.FILES.get("image")
		diary_idc = request.POST.get('diary_idc', "")
		diary_idj = request.POST.get('diary_idj', "")
		selected_groups = [diary_idc,diary_idj]

		qs = Content.objects.get(cno=cno)
		qs.ctitle = ctitle
		qs.ccontent = ccontent
		qs.cdate = cdate
		if image:
			qs.image = image
			

		if selected_groups[0]  ==  '' and  selected_groups[1]  == '':
			qs.group_diary.clear()
		else:
			# join된 일기장에만 공유
			if selected_groups[0] == '':
				jdiary = GroupDiary.objects.filter(gno=selected_groups[1]).first()
				qs.group_diary.add(jdiary)
			elif selected_groups[1] == '':
				cdiary = GroupDiary.objects.filter(gno=selected_groups[0]).first()
				qs.group_diary.add(cdiary)
			else:
				cdiary = GroupDiary.objects.filter(gno=selected_groups[0]).first()
				jdiary = GroupDiary.objects.filter(gno=selected_groups[1]).first()
				qs.group_diary.add(cdiary,jdiary)

		qs.save()

		return render(request,'dmodify.html',{'u_msg':cno})
	
	## 게시글 삭제

def ddelete(request, cno):
	if request.method == "POST":  # 요청 방식이 POST인지 확인
			# 세션에서 사용자 ID 가져오기
			session_id = request.session.get('session_id')
			member = Member.objects.filter(id=session_id).first()
			# 사용자와 게시글 작성자가 동일한지 확인
			content = Content.objects.filter(cno=cno, member=member).first()
			if not content:
					return HttpResponseForbidden("권한이 없거나 게시물이 존재하지 않습니다.")
			# 게시글 삭제
			content.delete()
			return JsonResponse({'status': 'success', 'message': '게시물이 삭제되었습니다.'})
	return JsonResponse({'status': 'error', 'message': '잘못된 요청입니다.'}, status=400)

## join 일기장 보기
def JdiaryList(request):
	if request.method == "GET":        
		# 세션에 저장된 ID 가져오기
		session_id = request.session.get('session_id')  # 세션에서 'session_id'를 가져옴

		# session_id를 기준으로 Member 찾기
		member = Member.objects.filter(id=session_id).first()
		qb = Img.objects.filter(id=session_id).first()

		if not member:
			return HttpResponse("사용자 정보가 존재하지 않습니다.", status=400)

		if member.joined_group:
			# Member 에서 join 다이어리 gno 가져오기
			gno = member.joined_group.gno
			joingroup = GroupDiary.objects.filter(gno=gno).first()
			
			# join다이어리의 Content 가져오기
			contents = joingroup.content_set.all().order_by("-cdate")  # 해당 GroupDiary에 연결된 모든 Content 객체 가져오기
			if not contents:
				return render(request, 'JdiaryList.html')

			npage = request.GET.get('npage', 1)
			paginator = Paginator(contents, 10)
			page_obj = paginator.get_page(npage)
			
			context = {
				'member':member,
				'content': page_obj.object_list,
				'JdiaryList':page_obj,
				'jdiary':contents,
				'joinDiary':joingroup,
				'qb':qb}
			return render(request, 'JdiaryList.html', context)
		else:
			context = {'qb':qb}
			return render(request, 'JdiaryList.html', context)
				
# create 일기장 보기
def CdiaryList(request):
	if request.method == "GET":
			id = request.session.get('session_id')  # 현재 사용자의 ID 가져오기
			# 현재 로그인한 사용자 확인
			member = Member.objects.filter(id=id).first()
			qb = Img.objects.filter(id=id).first()
			if not member:
					return HttpResponse("사용자 정보가 존재하지 않습니다.", status=400)
			if member.created_group:
				# 사용자가 만든 그룹 (created_group) 정보
				created_group = member.created_group
				# 사용자가 초대된 그룹 (joined_group) 정보
				joined_group = GroupDiary.objects.filter(gno=created_group.gno)
				# 사용자가 속한 그룹에 해당하는 모든 게시글 가져오기
				# 자신이 속한 그룹에 공유된 게시글 가져오기
				diaries = Content.objects.filter(group_diary=created_group,  # 그룹 다이어리 기준으로
						group_diary__isnull=False  # group_diary가 None이 아닌 게시글만
				).order_by('-cdate')  # 최신순 정렬
			else:
					diaries = None  # 그룹에 속하지 않으면 게시글 없음
					created_group = None  # 그룹정보 없음
			return render(request, 'CdiaryList.html', {
					'diaries': diaries,            # 다이어리 리스트
					'created_group': created_group,  # 그룹 정보
					'info': member,                  # 내정보
					'qb':qb,
			})
	

## 내 다이어리 삭제
def delete_all_posts(request):
	id = request.session.get('session_id')
	# Content의 다이어리 내용 삭제
	Content.objects.filter(member__id=id).delete()

	qs = MdiaryBoard.objects.get(id=id)
	qs.mtitle = "나의 일기장"
	qs.save()
	# 3,ccc,123,첫 일기장~~~,2024-12-31
	return render(request,'diaryHome.html',{"d_msg":"1"})


# 내 다이어리 제목 수정
def titleChg(request):
    if request.method == 'POST':
        mtitle = request.POST.get('mtitle')  # POST로 전달된 mtitle 값 가져오기

        # mtitle 값이 없거나 빈 값이면 에러 처리
        if not mtitle or mtitle.strip() == "":
            return JsonResponse({'error': '제목을 1글자 이상 입력해주세요.'}, status=400)

        # 세션에서 id 가져오기
        id = request.session.get('session_id')

        # 해당 id에 해당하는 다이어리 제목 업데이트
        MdiaryBoard.objects.filter(id=id).update(mtitle=mtitle.strip())

        # 성공 시 JSON 응답 반환
        return JsonResponse({'message': '다이어리 제목이 성공적으로 수정되었습니다.'})
    
    return JsonResponse({'error': '잘못된 요청 방식입니다.'}, status=405)  # POST만 처리하도록


## 가족 다이어리 삭제
def Cdelete_all_posts(request):
	id = request.session.get('session_id')
	member = Member.objects.filter(id=id).first()
	gno = member.created_group.gno
	GroupDiary.objects.filter(gno=gno).delete()

	return render(request,'diaryHome.html',{"cd_msg":"1"})


## 가족 다이어리 제목 수정
def CtitleChg(request):
	if request.method == 'POST':
		gtitle = request.POST.get('gtitle')

		if not gtitle or gtitle.strip() == "":
			return JsonResponse({'error': '제목을 1글자 이상 입력해주세요.'}, status=400)
		
		id = request.session.get('session_id')
		member = Member.objects.filter(id=id).first()
		gno = member.created_group.gno
		GroupDiary.objects.filter(gno=gno).update(gtitle=gtitle.strip())

		return JsonResponse({'message': '다이어리 제목이 성공적으로 수정되었습니다.'})
	
	return JsonResponse({'error': '잘못된 요청 방식입니다.'}, status=405)