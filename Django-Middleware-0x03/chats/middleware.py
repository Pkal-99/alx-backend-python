import logging
from datetime import datetime
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Set up logging
        logging.basicConfig(
            filename='user_requests.log',
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_message)
        return self.get_response(request)
class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the application based on the server time.
    Denies access between 9 PM (21:00) and 6 AM (06:00).
    """


    def __init__(self, get_response):
        """
        One-time configuration and initialization.
        get_response is the callable for the next middleware or view.
        """
        self.get_response = get_response
        # Define the access time windows
        self.ACCESS_START_HOUR = 6  # 6 AM
        self.ACCESS_END_HOUR = 21  # 9 PM (21:00)

    def __call__(self, request):
        """
        The code to be executed for each request before the view (and later middleware) is called.
        """
        now = datetime.datetime.now()
        current_hour = now.hour

        is_restricted_time = (current_hour >= self.ACCESS_END_HOUR) or \
                             (current_hour < self.ACCESS_START_HOUR)

        if is_restricted_time:
            # Deny access by returning an HTTP 403 Forbidden response
            print(f"Access denied at {now.strftime('%H:%M:%S')}. Outside of allowed hours (06:00 - 21:00).")
            return HttpResponseForbidden("Access is restricted. The chat is only available between 6 AM and 9 PM.")
            
        
        # If the time is within the allowed window, call the next component (middleware or view)
        response = self.get_response(request)

        # Code to be executed for each request/response after the view is called
        return response
    
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_log = defaultdict(list)  # {ip: [timestamps]}
        self.lock = Lock()
        self.limit = 5  # messages
        self.window = 60  # seconds

    def __call__(self, request):
        if request.method == 'POST' and request.path.startswith("/chats/"):
            ip = self.get_client_ip(request)
            now = time.time()

            with self.lock:
                # Remove timestamps older than the window
                self.request_log[ip] = [
                    t for t in self.request_log[ip] if now - t < self.window
                ]

                if len(self.request_log[ip]) >= self.limit:
                    return HttpResponseForbidden("403 Forbidden: Message rate limit exceeded (5 messages/minute).")

                self.request_log[ip].append(now)

        return self.get_response(request)
