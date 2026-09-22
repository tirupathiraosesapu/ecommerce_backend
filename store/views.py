from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse
from .models import Category, Product, Review
from .serializers import CategorySerializer, ProductSerializer, ProductDetailSerializer, ReviewSerializer

@extend_schema(
    tags=['Store - Categories'],
    summary='List all product categories',
    description='Returns a list of all product categories with metadata, image, icon identifier, and product counts.'
)
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

@extend_schema(
    tags=['Store - Products'],
    summary='List and filter products catalog',
    description='Returns a list of products with optional search, category filter, price range filtering, and ordering.',
    parameters=[
        OpenApiParameter(name='category', description='Filter by category name or category ID', required=False, type=str),
        OpenApiParameter(name='search', description='Search term for product name, description, or category', required=False, type=str),
        OpenApiParameter(name='min_price', description='Minimum price filter', required=False, type=float),
        OpenApiParameter(name='max_price', description='Maximum price filter', required=False, type=float),
        OpenApiParameter(
            name='ordering',
            description='Ordering parameter. Choices: price, -price, rating, -rating, created_at, -created_at, name, -name',
            required=False,
            type=str
        ),
    ]
)
class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Product.objects.all().select_related('category')
        
        # Category filter (by slug, name or id)
        category = self.request.query_params.get('category')
        if category:
            if category.isdigit():
                queryset = queryset.filter(category_id=int(category))
            else:
                queryset = queryset.filter(Q(category__slug__iexact=category) | Q(category__name__iexact=category))

        # Search filter (name or description)
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | 
                Q(description__icontains=search) |
                Q(category__name__icontains=search)
            )

        # Price range filter
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        # Sorting
        ordering = self.request.query_params.get('ordering', '-created_at')
        valid_orderings = ['price', '-price', 'rating', '-rating', 'created_at', '-created_at', 'name', '-name']
        if ordering in valid_orderings:
            queryset = queryset.order_by(ordering)

        return queryset

@extend_schema(
    tags=['Store - Products'],
    summary='List featured products',
    description='Returns curated flagship/featured products for the homepage showcase.'
)
class FeaturedProductListView(generics.ListAPIView):
    queryset = Product.objects.filter(is_featured=True).select_related('category')[:8]
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]

@extend_schema(
    tags=['Store - Products'],
    summary='Retrieve product details by ID',
    description='Returns full product details, category object, pricing, inventory stock, and all customer reviews.'
)
class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all().select_related('category').prefetch_related('reviews__user')
    serializer_class = ProductDetailSerializer
    permission_classes = [permissions.AllowAny]
    lookup_field = 'id'

@extend_schema(
    tags=['Store - Reviews'],
    summary='Submit a product review',
    description='Allows an authenticated user to write a rating (1-5 stars) and feedback comment for a product. Automatically recalculates the product overall rating. Requires Bearer JWT token.',
    request=ReviewSerializer,
    responses={
        201: OpenApiResponse(response=ReviewSerializer, description='Review posted successfully.'),
        400: OpenApiResponse(description='User has already reviewed this product or invalid rating.'),
        401: OpenApiResponse(description='Unauthorized. User must be authenticated to review.'),
        404: OpenApiResponse(description='Product not found.')
    }
)
class ProductReviewCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id):
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        user = request.user
        if Review.objects.filter(product=product, user=user).exists():
            return Response({"error": "You have already reviewed this product."}, status=status.HTTP_400_BAD_REQUEST)

        rating = request.data.get('rating', 5)
        comment = request.data.get('comment', '')

        try:
            rating = int(rating)
            if rating < 1 or rating > 5:
                raise ValueError()
        except ValueError:
            return Response({"error": "Rating must be an integer between 1 and 5."}, status=status.HTTP_400_BAD_REQUEST)

        review = Review.objects.create(
            product=product,
            user=user,
            rating=rating,
            comment=comment
        )

        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
