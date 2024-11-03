# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# from django.contrib.auth.models import User
# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated

# # Custom TokenObtainPairView for login
# class CustomTokenObtainPairView(TokenObtainPairView):
#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             # Generate tokens
#             tokens = serializer.validated_data
#             return Response({
#                 'access': tokens['access'],
#                 'refresh': tokens['refresh'],
#                 }
#             , status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# # View for refreshing tokens
# class CustomTokenRefreshView(TokenRefreshView):
#     def post(self, request, *args, **kwargs):
#         return super().post(request, *args, **kwargs)

# # Logout view (Optional)
# class LogoutView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         return Response({"detail": "Successfully logged out."}, status=status.HTTP_205_RESET_CONTENT)


from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework import viewsets, status
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from custom import Response
from users.models import User
from .utils import get_tokens
from .serializers import (
    UserLoginSerializer,
    EmptySerializer,
    ChangePasswordSerializer
)


class LoginView(GenericAPIView):
    """
    User Login.
    """

    queryset = User.objects.all()
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """
        User Login.

        Returns:
            {
            "access": access_token,
            "refresh": refresh_token,
            "role": role
            }
            in json format and in cookie.
        """
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data["username"]
            password = serializer.validated_data["password"]

            try:
                user = self.get_queryset().get(username=username)
            except User.DoesNotExist:
                return Response(
                    {"detail": "Username or password is not correct"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            if not user.check_password(password):
                return Response(
                    {"detail": "Username or password is not correct"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            access_token, refresh_token = get_tokens(user)

            response = Response()
            response.set_cookie(
                key="access",
                value=access_token,
                httponly=True,
                max_age=360000,
            )
            response.set_cookie(
                key="refresh",
                value=refresh_token,
                httponly=True,
                max_age=864000,
            )
            response.data = {
                "access": access_token,
                "refresh": refresh_token,
            }
            return response
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutView(GenericAPIView):
    """
    User Logout and Delete Cookie.
    """

    queryset = User.objects.all()
    serializer_class = EmptySerializer

    def post(self, request):
        """
        User Logout and Delete Cookie.
        """
        # TODO: add tokens to blacklist like in refresh view below
        # refresh_token = request.headers.get("Authorization") or request.COOKIES.get("refresh")
        # refresh.blacklist()

        response = Response()
        response.delete_cookie("access")
        response.delete_cookie("refresh")
        response.message = "logout succeeded"
        return response

class RefreshTokenView(GenericAPIView):
    """
    Token refresh view.
    """

    permission_classes = [AllowAny]
    serializer_class = EmptySerializer

    def post(self, request, *args, **kwargs):
        """
        Regenerate access and refresh tokens by using refresh token.
        """
        refresh_token = request.headers.get("Authorization") or request.COOKIES.get(
            "refresh"
        )

        if refresh_token:
            try:
                refresh = RefreshToken(refresh_token)
                refresh.blacklist()

                try:
                    user_id = refresh["user_id"]
                    user = User.objects.get(id=user_id)
                except:
                    return Response(
                        "User does not exist", status=status.HTTP_404_NOT_FOUND
                    )

                new_refresh_token = RefreshToken.for_user(user)
                new_access_token = str(new_refresh_token.access_token)

                response = Response()
                response.set_cookie(
                    key="access",
                    value=str(new_access_token),
                    httponly=True,
                    max_age=360000,
                )
                response.set_cookie(
                    key="refresh",
                    value=str(new_refresh_token),
                    httponly=True,
                    max_age=864000,
                )
                response.data = {
                    "access_token": new_access_token,
                    "refresh_token": str(new_refresh_token),
                }
                return response

            except TokenError as e:
                return Response(
                    {"detail": "Invalid refresh token"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(
            {"detail": "Refresh token not provided"}, status=status.HTTP_400_BAD_REQUEST
        )
        
class ChangePasswordView(GenericAPIView):
    """
    Change Password.
    """

    serializer_class = ChangePasswordSerializer

    def post(self, request, *args, **kwargs):
        """
        Change password by enter old and new password.
        """
        serializer = self.get_serializer(
            data=request.data, context={"request": request}
        )

        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data["new_password"])
            user.save()
            return Response(
                message="Password has been changed", status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)