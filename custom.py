from rest_framework import pagination
from rest_framework.response import Response as DRFResponse
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.authentication import JWTAuthentication


class Response(DRFResponse):
    """
    Custom Response Class.

    The changes is only adding message attribute to the Response to use it in
    CustomJSONRenderer class to format the JSON response and
    include message attribute in the response.
    """

    def __init__(
        self,
        data=None,
        message=None,
        status=None,
        template_name=None,
        headers=None,
        exception=False,
        content_type=None,
    ):

        self.message = message

        # Call the parent class constructor
        super().__init__(data, status, template_name, headers, exception, content_type)


class CustomPagination(pagination.PageNumberPagination):
    """Custom Pagination Class"""

    page_size = 5  # Default page size
    page_size_query_param = (
        "page_size"  # Allow clients to set page size via query param
    )
    max_page_size = 100  # Maximum allowed page size

    def get_paginated_response(self, data):
        """Customize the pagination response structure"""
        return Response(
            {
                "total_items": self.page.paginator.count,
                "total_pages": self.page.paginator.num_pages,
                "page_size": self.get_page_size(request=self.request),
                "current_page": self.get_page_number(self.request, self.page.paginator),
                "next": self.get_next_link(),
                "previous": self.get_previous_link(),
                "results": data,  # Paginated data
            }
        )

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication
    """

    def authenticate(self, request):
        """
        Custom authentication which checks if the token (in headers or in cookie) is valid
        """
        token = request.headers.get("Authorization") or request.COOKIES.get("access")

        if token:
            try:
                validated_token = self.get_validated_token(token)
                user = self.get_user(validated_token)
                request.user = user
                return (user, validated_token)
            except AuthenticationFailed:
                return None
        return None