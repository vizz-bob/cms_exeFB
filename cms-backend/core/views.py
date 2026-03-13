from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser 
from .serializers import UserRegistrationSerializer, UserProfileSerializer
from .models import UserProfile

User = get_user_model()

@api_view(['GET'])
@permission_classes([AllowAny])
def home(request):
    return Response({"message": "Welcome to XpertAI API System", "status": "Running"})

# ==========================================
#  SYSTEM SETUP & AUTH
# ==========================================

class SystemStatusView(APIView):
    """
    Checks if the system has at least one superuser configured.
    Used by the frontend to decide whether to show Login or Setup screen.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        is_setup_complete = User.objects.filter(is_superuser=True).exists()
        return Response({"is_setup_complete": is_setup_complete})

class SetupAdminView(APIView):
    """
    Creates the first superuser. Fails if one already exists.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        if User.objects.filter(is_superuser=True).exists():
            return Response(
                {"error": "Setup already complete. Admin exists."}, 
                status=status.HTTP_403_FORBIDDEN
            )

        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Username and Password are required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.create_superuser(
                username=username, 
                email=email, 
                password=password
            )
            return Response({
                "message": "Admin account created successfully! Please log in.",
                "username": user.username
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully!",
                "user_id": user.id,
                "username": user.username,
                "role": request.data.get('role', 'client')
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomLoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        role = "client"
        if hasattr(user, 'profile'):
            role = user.profile.role
        elif hasattr(user, 'client_profile'):
            role = 'client'
        elif hasattr(user, 'professional_profile'):
            role = 'professional'

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'role': role
        })

class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    Standard Profile View (Stats Removed)
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserProfileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        # Automatically get profile for current user
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile