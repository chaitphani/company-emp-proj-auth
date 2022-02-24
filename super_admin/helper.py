from super_admin.models import User
from common.authentication import RefreshToken


def get_token_data(user: User):
    refresh = RefreshToken.for_user(user)
    return {
        # "refresh": str(refresh),
        "access": str(refresh.access_token),
        "id": str(user.id),
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "user_type": user.user_type,
    }