from django.http import HttpRequest


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print("request count:", self.requests_count)
        response = self.get_response(request)
        self.responses_count += 1
        print("response count:", self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print(f"exception count:", self.exceptions_count)
