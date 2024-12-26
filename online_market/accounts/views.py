from django.shortcuts import render, redirect
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
)
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import (
    require_POST,
    require_http_methods,
)
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, CustomUserCreationForm

@require_http_methods(["GET", "POST"])  # GET, POST 요청받을 때만 login 실행
def login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())    # 로그인
            next_url = request.GET.get("next") or "home"    # 로그인 성공하면 이동하려던 곳, 실패하면 홈 이동
            return redirect(next_url)
    else:        
        form = AuthenticationForm()
    context = {"form": form}
    return render(request, "accounts/login.html", context)

@require_POST   # POST 요청 시에만 logout 실행
def logout(request):
    if request.user.is_authenticated:   # user가 로그인이 된 상태라면
        auth_logout(request)    # 로그아웃
    return redirect("home")

@require_http_methods(["GET", "POST"])
def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # 새유저 정보 저장
            auth_login(request, user)   # 가입함과 동시에 로그인
            return redirect("home")
    else:
        form = CustomUserCreationForm()
    context = {"form": form}
    return render(request, "accounts/signup.html", context)

@require_POST
def delete(request):
    if request.user.is_authenticated:
        request.user.delete()   # 회원 탈퇴
        auth_logout(request)    # 세션 지우기
    return redirect("home")

@require_http_methods(["GET", "POST"])
def update(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("home")
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {"form": form}
    return render(request, "accounts/update.html", context)

@login_required
@require_http_methods(["GET", "POST"])
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect("home")
    else:
        form = PasswordChangeForm(request.user)
    context = {"form": form}
    return render(request, "accounts/change_password.html", context)