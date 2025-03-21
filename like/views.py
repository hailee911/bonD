from django.http import JsonResponse
from .models import Like, Content, Member

def like(request, cno):
    if request.method == 'POST':
        session_id = request.session.get('session_id')  # 세션에서 사용자 정보 가져오기
        member = Member.objects.filter(id=session_id).first()
        
        if not member:
            return JsonResponse({'success': False, 'message': '사용자 정보 없음'}, status=400)
        
        content = Content.objects.get(cno=cno)  # 좋아요를 누른 게시글 가져오기
        
        # 좋아요가 이미 있다면 취소
        like_obj = Like.objects.filter(content=content, member=member).first()
        
        if like_obj:
            like_obj.delete()  # 모델에서 삭제제
            liked = False
        else:
            # 좋아요가 없다면 새로 생성
            Like.objects.create(content=content, member=member)
            liked = True

        # 좋아요 갯수 계산
        like_count = Like.objects.filter(content=content).count()

        return JsonResponse({
            'success': True,
            'liked': liked,
            'like_count': like_count
        })
    return JsonResponse({'success': False}, status=400)
