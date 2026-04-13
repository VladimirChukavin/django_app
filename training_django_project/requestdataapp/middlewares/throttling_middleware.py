import time
from django.http import HttpRequest, HttpResponseForbidden

ip_request_times = {}
THROTTLE_INTERVAL = 2


class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        client_ip = request.META.get("REMOTE_ADDR")
        current_time = time.time()

        if client_ip in ip_request_times:
            time_diff = current_time - ip_request_times[client_ip]
            if time_diff < THROTTLE_INTERVAL:
                return HttpResponseForbidden(
                    "Слишком много запросов. Попробуйте позже."
                )

        ip_request_times[client_ip] = current_time

        response = self.get_response(request)
        return response
