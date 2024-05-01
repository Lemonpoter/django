# accounts/views.py
from django.contrib.auth import get_user_model,authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render
import json

User = get_user_model()

@method_decorator(csrf_exempt, name='dispatch')
class SignUpView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        nickname = data.get('nickname')
        birthday = data.get('birthday')
        gender = data.get('gender')
        bio = data.get('bio')

        # 필수 필드가 모두 전달되었는지 확인
        if not all([username, email, password, name, nickname, birthday]):
            return JsonResponse({'error': '모든 필드는 필수입니다.'}, status=400)

        # username과 email이 이미 사용 중인지 확인
        if User.objects.filter(username=username).exists():
            return JsonResponse({'error': '이미 사용 중인 사용자명입니다.'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'error': '이미 사용 중인 이메일입니다.'}, status=400)

        # 사용자 생성
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=name,
            last_name=nickname,
            birthday=birthday,
            gender=gender,
            bio=bio
        )
        user.save()

        return JsonResponse({'success': '회원가입이 완료되었습니다.'})


class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        # POST 요청으로부터 사용자명(username)과 비밀번호(password)를 가져옴
        username = request.POST.get('username')
        password = request.POST.get('password')

        # 사용자 인증(authentication)을 시도함
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # 사용자 인증에 성공하면 세션에 사용자 정보를 저장하고 로그인 상태로 만듦
            login(request, user)
            return JsonResponse({'message': '로그인 성공'})
        else:
            # 사용자 인증에 실패하면 적절한 에러 메시지를 반환
            return JsonResponse({'error': '로그인 실패. 사용자명 또는 비밀번호가 잘못되었습니다.'}, status=400)


def signup(request):
    return render(request, 'accounts/signup.html')

def register(request):
    return render(request, 'register.html')