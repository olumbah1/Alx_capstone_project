from rest_framework import generics, status
from .serializers import UserLoginSerializer, UserRegistrationSerializer, UserProfileSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout

# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    # Register a new user account
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            #create token for new user
            token, created = Token.objects.get_or_create(user=user)
            
            return Response({
                'message': 'User created successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'token':token.key
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(generics.GenericAPIView):
        """Login user and return token"""
        serializer_class = UserLoginSerializer
        permission_classes = [AllowAny]
        
        def post(self, request):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                user = serializer.validated_data['user']
                # Get or create token
                token, created = Token.objects.get_or_create(user=user)
                
                # Login user (for session-based auth if needed)
                login(request, user)
                
                return Response({
                    'message': 'Login Successful',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                         
                    },
                    "token": token.key
                }, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(generics.GenericAPIView):
        """Logout user and delete token"""
        permission_classes = [IsAuthenticated]
        
        def post(self, request):
            try:
                # Delete the user's token
                request.user.auth_token.delete()
                
                # Logout user (for session-based auth)
                logout(request)
                return Response({
                    'message': 'Logout successful'
                }, status=status.HTTP_200_OK)
            except:
                return Response({
                    'error': 'Error logging out'
                }, status=status.HTTP_400_BAD_REQUEST)
                
class UserProfileView(generics.RetrieveUpdateAPIView):
    """Get and update user profile"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user               