from django.urls import path
from . import views

app_name = 'products'
urlpatterns = [
    path('home/', views.home, name="home"),
    #
    path('', views.products, name='products'),
    path('<int:pk>/', views.product_detail, name='product_detail'),
    path('<int:pk>', views.like, name='like'),
    #
    path('create', views.create, name='create'),
    path('<int:pk>/update/', views.update, name='update'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    #
]