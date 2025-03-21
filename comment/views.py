from django.shortcuts import redirect
from comment.models import Comment
from diary.models import Content
from loginpage.models import Member
from django.utils.timezone import now
from django.urls import reverse

def add_comment(request, cno):
	if request.method == "POST":
		# 세션에서 현재 로그인한 사용자 정보 가져오기
		session_id = request.session.get('session_id')
		if not session_id:
			return redirect('/loginpage/login/')  # 로그인 페이지로 리다이렉트

		member = Member.objects.filter(id=session_id).first()
		if not member:
			return redirect('/loginpage/login/')

		# 연결된 게시글 가져오기
		content = Content.objects.filter(cno=cno).first()
		# if not content:
		#     return redirect('diary_view')  # 게시글 목록 페이지로 리다이렉트

		previous_url = request.META.get('HTTP_REFERER', '') # 바로 이전 url
		group_num = None  # 기본값 설정
		print('댓글이 달린 페이지',previous_url)

		# URL에 따라 group_num 설정
		if 'Cdiary_view' in previous_url:  # Cdiary_view
			if member.created_group:  # member.created_group이 존재하는지 확인
				group_num = member.created_group.gno  # 사용자가 만든 그룹의 gno
		elif 'Jdiary_view' in previous_url:  # Jdiary_view
			if member.joined_group:  # member.joined_group이 존재하는지 확인
				group_num = member.joined_group.gno  # 사용자가 초대된 그룹의 gno
		

		# 폼에서 입력된 댓글 내용 가져오기
		text = request.POST.get('comment_text', '').strip()
		if text:
			# 댓글 저장
			Comment.objects.create(
				content=content,
				member=member,
				text=text,
				created_at=now(),
				updated_at=now(),
				group_num = group_num,
			)


		if 'Cdiary_view' in previous_url:  # Cdiary_view
			link = 'Cdiary_view'
		elif 'Jdiary_view' in previous_url:  # Jdiary_view
			link = 'Jdiary_view'
		else:
			link = 'diary_view'
			
		# 댓글 작성 후 원래 페이지로 리다이렉트
		# 저장 후 페이지 새로고침
		# 댓글 작성 후 원래 게시글 페이지로 리다이렉트, comment_success 파라미터 추가
		return redirect(reverse(f'diary:{link}', kwargs={'cno': cno}) + '?comment_success=true')

# comment/views.py
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

@require_http_methods(["POST"])
def delete_comment(request, comment_id):
	# 댓글을 찾습니다
	comment = get_object_or_404(Comment, pk=comment_id)
	# 댓글 삭제
	comment.delete()

	# 삭제 후 JSON 응답 반환
	return JsonResponse({'status': 'success', 'message': '댓글이 삭제되었습니다.'})
