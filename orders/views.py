from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .models import Order
from .serializers import OrderSerializer, CreateOrderSerializer

@extend_schema(
    tags=['Orders & Checkout'],
    summary='Create and place an order',
    description='Places a new customer order with line items, shipping address, and payment method. Automatically computes subtotal, sales tax, shipping fee, deducts product stock, and associates the order with the authenticated user. Requires Bearer JWT token.',
    request=CreateOrderSerializer,
    responses={
        201: OpenApiResponse(response=OrderSerializer, description='Order created successfully.'),
        400: OpenApiResponse(description='Validation error or missing required fields.'),
        401: OpenApiResponse(description='Unauthorized. Requires Bearer JWT token.')
    }
)
class CreateOrderView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        output_serializer = OrderSerializer(order)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)

@extend_schema(
    tags=['Orders & Checkout'],
    summary='List current user orders',
    description='Returns a list of all historical orders placed by the currently logged-in user, ordered by most recent first. Requires Bearer JWT token.',
    responses={
        200: OrderSerializer(many=True),
        401: OpenApiResponse(description='Unauthorized. Requires Bearer JWT token.')
    }
)
class MyOrdersListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).prefetch_related('items')

@extend_schema(
    tags=['Orders & Checkout'],
    summary='Retrieve detailed order invoice by ID',
    description='Retrieves the complete receipt and delivery status for a specific order. Authenticated users can only view their own orders; staff members can view any order. Requires Bearer JWT token.',
    responses={
        200: OrderSerializer,
        401: OpenApiResponse(description='Unauthorized.'),
        404: OpenApiResponse(description='Order not found.')
    }
)
class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Order.objects.all().prefetch_related('items')
        return Order.objects.filter(user=user).prefetch_related('items')
