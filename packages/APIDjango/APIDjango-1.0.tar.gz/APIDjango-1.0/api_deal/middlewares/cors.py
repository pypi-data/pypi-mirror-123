from django.utils.deprecation import MiddlewareMixin

ACCESS_CONTROL_ALLOW_ORIGIN = "Access-Control-Allow-Origin"
ACCESS_CONTROL_EXPOSE_HEADERS = "Access-Control-Expose-Headers"
ACCESS_CONTROL_ALLOW_CREDENTIALS = "Access-Control-Allow-Credentials"
ACCESS_CONTROL_ALLOW_HEADERS = "Access-Control-Allow-Headers"
ACCESS_CONTROL_ALLOW_METHODS = "Access-Control-Allow-Methods"
ACCESS_CONTROL_MAX_AGE = "Access-Control-Max-Age"
default_headers = (
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
)

default_methods = ("DELETE", "GET", "OPTIONS", "PATCH", "POST", "PUT")

default_expose_headers = ("Content-Disposition", "Export-FileName")


class MyCorsMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        """
        Add the respective CORS headers
        """
        if request.method == "OPTIONS":
            response[ACCESS_CONTROL_ALLOW_HEADERS] = ", ".join(default_headers)
            response[ACCESS_CONTROL_ALLOW_METHODS] = ", ".join(default_methods)
        response[ACCESS_CONTROL_ALLOW_ORIGIN] = "*"
        response[ACCESS_CONTROL_EXPOSE_HEADERS] = ", ".join(default_expose_headers)
        return response
