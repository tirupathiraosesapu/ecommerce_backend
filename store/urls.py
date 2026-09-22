from django.urls import path
from .views import (
    CategoryListView,
    ProductListView,
    FeaturedProductListView,
    ProductDetailView,
    ProductReviewCreateView
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('products/featured/', FeaturedProductListView.as_view(), name='featured_products'),
    path('products/<int:id>/', ProductDetailView.as_view(), name='product_detail'),
    path('products/<int:product_id>/reviews/', ProductReviewCreateView.as_view(), name='product_review_create'),
]
