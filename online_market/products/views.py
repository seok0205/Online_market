from django.shortcuts import render, redirect, get_object_or_404
from .models import Product
from django.views.decorators.http import require_POST, require_http_methods
from django.contrib.auth.decorators import login_required
from .forms import ProductForm

def home(request):
    return render(request, 'products/home.html')

def products(request):
    products = Product.objects.all().order_by("-pk")
    context = {
        "products": products
    }
    return render(request, "products/products.html", context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {
        "product": product
    }
    return render(request, "products/product_detail.html", context)

@require_POST
def like(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        if product.like_users.filter(pk=request.user.pk).exists():
            product.like_users.remove(request.user)
        else:
            product.like_users.add(request.user)
    else:
        return redirect("accounts:login")
    
    return redirect("products:products")

@login_required
def create(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)  # 데이터가 바인딩된(값이 채워진) Form
        if form.is_valid():  # Form이 유효하다면 데이터를 저장하고 다른 곳으로 redirect
            product = form.save(commit=False)
            product.author = request.user
            product.save()
            return redirect("products:product_detail", product.pk)
    # 기존 new 함수 부분
    else:
        form = ProductForm()

    context = {"form": form}
    return render(request, "products/create.html", context)

@login_required
@require_http_methods(["GET", "POST"])
def update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.author == request.user:
        if request.method == "POST":    # instance라는 속성에 값이 있으면 instance 수정
            form = ProductForm(request.POST, instance=product)
            if form.is_valid():
                product = form.save()
                return redirect("products:product_detail", product.pk)
        else:   # 없으면 새로 생성
            form = ProductForm(instance=product)
    else:
        return redirect("products:products")

    context = {
        "form": form,
        "product": product,
    }
    return render(request, "products/update.html", context)

@require_POST
def delete(request, pk):
    if request.user.is_authenticated:
        product = get_object_or_404(Product, pk=pk)
        if product.author == request.user:
            product.delete()
    return redirect("products:products")