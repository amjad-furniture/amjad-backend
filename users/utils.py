from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens(user):
    """
    Get access and refresh token for the given user.
    """
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)

    return access_token, refresh_token
