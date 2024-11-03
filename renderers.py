from rest_framework.renderers import JSONRenderer


class CustomJSONRenderer(JSONRenderer):
    """
    A custom renderer that formats the JSON response to include
    status, message, data, and error fields.
    """

    def render(self, data, accepted_media_type=None, renderer_context=None):

        # Access the response object
        response = renderer_context.get("response")

        # Handle error cases (status code not in the 200-299 range)
        if response and not (200 <= response.status_code < 300):
            # Prepare the response data structure
            response_data = {
                "status": "error",
                "error": data,
            }

            return super().render(response_data, accepted_media_type, renderer_context)

        # Default message
        message = "Request succeeded"

        # Check if the response object has a custom message
        try:
            if response.message:
                message = response.message
        except:
            pass

        # Handle pagination response format
        if isinstance(data, dict) and "results" in data:

            # Prepare the paginated response data structure
            response_data = {
                "status": "success",
                "message": message,
                "total_items": data.get("total_items"),
                "total_pages": data.get("total_pages"),
                "page_size": data.get("page_size"),
                "current_page": int(data.get("current_page")),
                "next": data.get("next"),
                "previous": data.get("previous"),
                "data": data.get("results"),
            }

        else:
            # Non-paginated response structure
            response_data = {
                "status": "success",
                "message": message,
                "data": data,
            }

        # disable cross-origin policy remember to delete this line
        # response["Cross-Origin-Opener-Policy"] = "unsafe-none"

        # Call the parent class's render method to convert the Python dict to JSON
        return super().render(response_data, accepted_media_type, renderer_context)
