from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from accounts.models import User
from products.models import Product

def users(request):
    users = User.objects.all().order_by("id")
    context = {"users": users}
    return render(request, "users/users.html", context)

def profile(request, username):
    member = get_object_or_404(get_user_model(), username=username)
    products = Product.objects.filter(author_id=member.pk)
    like_products = Product.objects.filter(like_users=member.pk)
    context = {
        "member": member,
        "products": products,
        "like_products": like_products,
    }
    return render(request, "users/profile.html", context)

@require_POST
def follow(request, user_id):
    # request.user == "현재 로그인한 사람"
	# member == "누군가의 프로필"
    if request.user.is_authenticated:
        member = get_object_or_404(get_user_model(), pk=user_id)
        if request.user != member:  # 자기 자신을 팔로우하는 경우 제외 
            if request.user in member.followers.all():
                member.followers.remove(request.user)
            else:
                member.followers.add(request.user)
        return redirect("users:profile", member.username)
    return redirect("accounts:login")