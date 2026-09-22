from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import User
from drf_spectacular.utils import extend_schema, OpenApiResponse
from .serializers import RegisterSerializer, UserSerializer, CustomTokenObtainPairSerializer

@extend_schema(
    tags=['Authentication'],
    summary='Obtain JWT Token Pair (Login)',
    description='Authenticates a user with username and password. Returns access token, refresh token, and user profile data.',
    responses={
        200: OpenApiResponse(
            description='Login successful. Returns access and refresh JWT tokens alongside user profile information.'
        ),
        401: OpenApiResponse(description='Invalid credentials provided.')
    }
)
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

@extend_schema(
    tags=['Authentication'],
    summary='Register a new user account',
    description='Creates a new user record and auto-initializes their user profile in the database.',
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(
            response=UserSerializer,
            description='User registered successfully.'
        ),
        400: OpenApiResponse(description='Validation errors (e.g. username/email already taken or mismatched passwords).')
    }
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = UserSerializer(user).data
        return Response({
            "message": "User registered successfully",
            "user": user_data
        }, status=status.HTTP_201_CREATED)

@extend_schema(
    tags=['User Profile'],
    summary='Get or update authenticated user profile',
    description='Retrieves or updates personal information (first name, last name, email) and shipping profile details (phone, street address, city, postal code). Requires Bearer JWT token.',
    responses={
        200: UserSerializer,
        401: OpenApiResponse(description='Authentication credentials were not provided or are invalid.')
    }
)
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
