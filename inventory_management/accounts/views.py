from rest_framework import generics, status
from .serializers import UserLoginSerializer, UserRegistrationSerializer, UserProfileSerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'User created successfully',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'message': 'Login Successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
           
            refresh_token = request.data.get("refresh")
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  
                
                return Response({
                    'message': 'Logout successful'
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'error': 'Refresh token required'
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                'error': 'Error logging out'
            }, status=status.HTTP_400_BAD_REQUEST)

class TokenRefreshView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response({
                    'error': 'Refresh token required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            refresh = RefreshToken(refresh_token)
            return Response({
                'access': str(refresh.access_token),
                'message': 'Token refreshed successfully'
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': 'Invalid refresh token'
            }, status=status.HTTP_400_BAD_REQUEST)

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    

class ChangePasswordView(generics.GenericAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Password changed successfully'
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)