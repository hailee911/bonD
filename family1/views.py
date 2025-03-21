from django.shortcuts import render
from loginpage.models import Member
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from diary.models import GroupDiary
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from mypage.models import Img


@csrf_exempt  # 테스트 시 CSRF 검증 해제 (프로덕션 환경에서는 사용 금지)
def add_member(request):
    id = request.session.get('session_id')
    if not id:
        return JsonResponse({'error': '로그인이 필요합니다.'}, status=400)

    member_id = request.POST.get('member_id')
    if not member_id:
        return JsonResponse({'error': '멤버 ID를 입력하세요.'}, status=400)

    try:
        user = get_object_or_404(Member, id=id)
        group_diary = GroupDiary.objects.filter(member=user, role=1).first()

        if not group_diary:
            return JsonResponse({'error': '그룹이 없습니다. 먼저 그룹을 생성하세요.'}, status=400)

        add_member2 = get_object_or_404(Member, id=member_id)

        if add_member2.joined_group:
            return JsonResponse({'error': '이미 다른 그룹에 속해 있습니다.'})

        # 멤버 추가
        GroupDiary.objects.create(gno=group_diary.gno, member=add_member2, role=2, gtitle= group_diary.gtitle)
        add_member2.joined_group = group_diary
        add_member2.save()

        return JsonResponse({'success': '멤버가 추가되었습니다.'})

    except Member.DoesNotExist:
        return JsonResponse({'error': '멤버를 찾을 수 없습니다.'}, status=404)

    except Exception as e:
        return JsonResponse({'error': f'서버 에러: {str(e)}'}, status=500)


@require_POST
def delete_member(request, member_id):
    print(f"Attempting to delete member with ID: {member_id}")  # 멤버 ID 로그 출력
    
    id = request.session.get('session_id')
    if not id:
        print("No session ID found.")  # 세션 ID 로그
        return JsonResponse({'error': '로그인이 필요합니다.'}, status=400)

    # 삭제하려는 멤버와 로그인한 멤버가 동일한지 확인
    if str(id) == str(member_id):
        # 자기 자신을 삭제하려 할 때
        return JsonResponse({'error': '자기 자신은 삭제할 수 없습니다.'}, status=400)
    
    try:
        # 삭제할 멤버 찾기
        member = get_object_or_404(Member, id=member_id)
        print(f"Found member: {member.name}")  # 멤버 이름 출력

        if member.joined_group:
            print(f"Member is in group {member.joined_group}")  # 그룹 이름 출력
            group_diary = GroupDiary.objects.filter(member=member, gno=member.joined_group.gno).first()
            if group_diary:
                print(f"Deleting group diary for member {member.name}")  # 그룹 다이어리 삭제 출력
                group_diary.delete()

            member.joined_group = None
            member.save()
            print(f"Member {member.name}'s group removed.")  # 멤버 그룹 제거 출력
            return JsonResponse({'success': '멤버가 삭제되었습니다.'})
        else:
            print(f"Member {member.name} is not in a group.")  # 그룹에 속하지 않은 경우
            return JsonResponse({'error': '삭제할 멤버는 그룹에 속해 있지 않습니다.'}, status=400)

    except Member.DoesNotExist:
        print(f"Member with ID {member_id} does not exist.")  # 멤버를 찾을 수 없는 경우
        return JsonResponse({'error': '멤버를 찾을 수 없습니다.'}, status=404)
    except Exception as e:
        print(f"Error: {str(e)}")  # 기타 예외 발생 시 출력
        return JsonResponse({'error': f'서버 에러: {str(e)}'}, status=500)



def fam(request):
    # 현재 로그인한 사용자 ID 가져오기
    id = request.session.get('session_id')
    if not id:
        return render(request, 'login.html', {'error': '로그인이 필요합니다.'})
    
    try:
        # 사용자 정보 가져오기
        user = Member.objects.get(id=id)
    except Member.DoesNotExist:
        return render(request, 'fam.html', {'error': '사용자를 찾을 수 없습니다.'})

    # 생성된 그룹과 가입된 그룹 가져오기
    created_group = user.created_group or ''
    joined_group = user.joined_group or ''
    
    # 쉼표로 분리하여 리스트로 변환
    created_group_list = list(str(created_group).split(','))
    joined_group_list = list(str(joined_group).split(','))

    # 리스트 길이 확인 후 안전하게 요소 가져오기
    created_group_name = created_group_list[2] if len(created_group_list) > 2 else None
    joined_group_name = joined_group_list[2] if len(joined_group_list) > 2 else None

    # 같은 그룹에 가입된 멤버들 가져오기
    # members = GroupDiary.objects.all()
    # you_2 = GroupDiary.objects.filter(role = 1) & GroupDiary.objects.filter(member__id = id)
    # join_goup = GroupDiary.objects.filter(gno = you_2.gno)
    # print("you_2:",you_2)
    # print("너의 그룹:",join_goup)

    # 사용자가 생성한 그룹 찾기
    created_group_diary = GroupDiary.objects.filter(member=user, role=1).first()
    joined_group_members = []
    if created_group_diary:
      joined_group_members = GroupDiary.objects.filter(gno=created_group_diary.gno)

    # 사용자가 가압한 그룹 찾기
    joined_group_diary = GroupDiary.objects.filter(member=user, role=2).first()
    created_group_members = []
    if joined_group_diary:
      created_group_members = GroupDiary.objects.filter(gno=joined_group_diary.gno)


    # members = GroupDiary.objects.filter(member__id=id).first()
    # c_group = GroupDiary.objects.filter(gno = members.gno) & GroupDiary.objects.filter(role = 1)
    # print("gkasdfgk",c_group)
    # print("아이디",members)
    # joined_group_members = Member.objects.filter(joined_group=created_group) if created_group else []
    # if not joined_group_members:user.created_group = None
    # if not joined_group_members:created_group = None

    # 같은 그룹에 가입된 멤버들 가져오기2


    # created_group_members = Member.objects.filter(Q(created_group=joined_group) | Q(joined_group=joined_group)).exclude(id=id) if joined_group else []
    # created_group_members1 = Member.objects.filter(created_group=joined_group) if joined_group else []
    # if not created_group_members1:user.joined_group = None
    # if not created_group_members1:joined_group = None
    # user.save()

    created_group_members_with_img = []
    for member in created_group_members:
        img_obj = Img.objects.filter(id=member.member.id).first()
        created_group_members_with_img.append({
            'member': member.member,
            'img': img_obj.img.url if img_obj and img_obj.img else '../static/images/calendar1/default_profile.png'
        })
    joined_group_members_with_img = []
    for member in joined_group_members:
        img_obj = Img.objects.filter(id=member.member.id).first()
        joined_group_members_with_img.append({
            'member': member.member,
            'img': img_obj.img.url if img_obj and img_obj.img else '../static/images/calendar1/default_profile.png'
        })


    # 그룹 존재 여부 확인
    has_group = bool(created_group or joined_group)
    qb = Img.objects.filter(id=id).first()
    # 컨텍스트 데이터 구성
    context = {
        'user':user,
        'has_group': has_group,
        'created_group': created_group,
        'joined_group': joined_group,
        'created_group_name': created_group_name,
        'joined_group_name': joined_group_name,
        'joined_group_members': joined_group_members_with_img,
        'created_group_members': created_group_members_with_img,
        "qb":qb,
    }

    return render(request, 'fam.html', context)