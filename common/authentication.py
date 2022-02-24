from rest_framework.permissions import IsAuthenticated
from super_admin.models import User
from rest_framework_simplejwt.tokens import BlacklistMixin, Token
from task_project import settings
from common.helper import check_company_admin_permissions, check_employee_permissions


class IsAuthenticatedOverride(IsAuthenticated):
    def has_permission(self, request, view):
        try:
            user = request.user
            if not bool(user and user.is_authenticated):
                return False
                
            if user.user_type in [User.UserTypes.ADMIN]:
                return True
            if user.user_type == User.UserTypes.COMPANY_ADMIN:
                return check_company_admin_permissions(request)
            if user.user_type == User.UserTypes.EMPLOYEE:
                return check_employee_permissions(request)

            return False
        except Exception as err:
            print(f"IsAuthenticatedOverride: {err}", exc_info=True)
            return False


class RefreshToken(BlacklistMixin, Token):
    
    token_type = "refresh"
    lifetime = settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]

    no_copy_claims = (
        settings.SIMPLE_JWT["TOKEN_TYPE_CLAIM"],
        settings.SIMPLE_JWT["JTI_CLAIM"],
    )

    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token["id"] = str(user.id)
        return token

    @property
    def access_token(self):
        access = AccessToken()
        access.set_exp(from_time=self.current_time)
        no_copy = self.no_copy_claims
        for claim, value in self.payload.items():
            if claim in no_copy:
                continue
            access[claim] = value
        return access


class AccessToken(Token):
    token_type = "access"
    lifetime = settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]
