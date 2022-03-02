from super_admin.models import User
from rest_framework import viewsets,status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from super_admin.helper import get_token_data


class RegisterAPI(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        try:
            try:
                User.objects.get(user_type=User.UserTypes.ADMIN)
                return Response({"User already exist cannot create another"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except User.DoesNotExist:
                pass

            user = User(
                first_name=request.data["first_name"],
                last_name=request.data["last_name"],
                email=request.data["email"],
                phone=request.data["phone"],
                is_active=True,
                user_type=User.UserTypes.ADMIN,
            )
            user.set_password(request.data["password"])
            user.save()
            return Response(
                get_token_data(user),
                status=status.HTTP_201_CREATED
            )
        except Exception as err:
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginAPI(viewsets.ViewSet):

    permission_classes = (AllowAny,)
    def create(self, request, *args, **kwargs):
        try:
            user = authenticate(
                username=request.data["email"], password=request.data["password"]
            )
            if not user:
                return Response(
                    {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
                )
            return Response(get_token_data(user),status=status.HTTP_200_OK)
        except Exception as err:
            print(f"Login create: {err}")
            return Response(err, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


