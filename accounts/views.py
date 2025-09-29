# accounts/views.py
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, UserSerializer
from django.utils import translation
from .serializers import UserProfileSerializer
from django.conf import settings
from django.utils.translation import gettext_lazy as _





User = get_user_model()

# 1) Register
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        # return JWT tokens on register
        refresh = RefreshToken.for_user(user)
        data = {
            "user": UserSerializer(user).data,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }
        return Response(data, status=status.HTTP_201_CREATED)

# 2) Custom Token obtain to include user data in response
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        # اضافه کردن اطلاعات کاربر به پاسخ
        data["user"] = UserSerializer(self.user).data
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

# 3) Logout (blacklist refresh token)
@csrf_exempt
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data.get("refresh")
        if refresh_token:
            from rest_framework_simplejwt.tokens import RefreshToken
            token = RefreshToken(refresh_token)
            token.blacklist()
        return Response({"message": _("Successfully logged out")}, status=status.HTTP_205_RESET_CONTENT)
    except Exception:
        return Response({"error": _("Invalid token")}, status=status.HTTP_400_BAD_REQUEST)

# 4) Profile GET / PATCH
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

def auth_test_view(request):
    return render(request, "accounts/auth_test_full.html")

class LanguagesView(APIView):
    """
    GET /api/accounts/languages/
    Returns available languages from settings.LANGUAGES as [{'code':'en','name':'English'}, ...]
    """
    permission_classes = [AllowAny]

    def get(self, request):
        langs = [{"code": code, "name": name} for code, name in getattr(settings, "LANGUAGES", [])]
        return Response(langs)

class UserLanguageUpdateView(APIView):
    """
    PATCH /api/accounts/me/language/
    Body: {"preferred_language": "fa"}  (or {"language":"fa"})
    Validates against settings.LANGUAGES and sets user.preferred_language.
    Also activates language for current request (and stores it in session if available).
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        lang = request.data.get("preferred_language") or request.data.get("language")
        if not lang:
            return Response({"detail": _("preferred_language is required")}, status=status.HTTP_400_BAD_REQUEST)

        # allowed codes
        allowed = [code for code, _ in getattr(settings, "LANGUAGES", [])]
        if lang not in allowed:
            return Response({"detail": _("Invalid language. Allowed: %(allowed)s") % {"allowed": allowed}}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        user.preferred_language = lang
        user.save()

        # activate for current request
        translation.activate(lang)
        request.LANGUAGE_CODE = lang
        # if sessions enabled, persist selection in session
        try:
            request.session[translation.LANGUAGE_SESSION_KEY] = lang
        except Exception:
            # if no session backend or using stateless tokens, ignore
            pass

        serializer = UserProfileSerializer(user, context={"request": request})
        resp = Response(serializer.data)
        resp["Content-Language"] = lang
        return resp

def languages_test_view(request):
    return render(request, "accounts/languages_test.html")

