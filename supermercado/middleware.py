import time
from django.http import HttpResponseForbidden
from django.core.cache import cache

class RateLimitMiddleware:
    """
    Middleware para limitar tentativas de login baseado no endereço IP.
    Isso ajuda a prevenir ataques de força bruta.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/accounts/login/' and request.method == 'POST':
            ip_address = self.get_client_ip(request)
            
            cache_key = f'login_attempt_{ip_address}'
            
            login_attempts = cache.get(cache_key, {'count': 0, 'timestamp': time.time()})
            
            current_time = time.time()
            if current_time - login_attempts['timestamp'] > 900:
                login_attempts = {'count': 0, 'timestamp': current_time}
            
            login_attempts['count'] += 1
            
            cache.set(cache_key, login_attempts, 900)
            
            if login_attempts['count'] > 5:
                return HttpResponseForbidden("Muitas tentativas de login. Por favor, tente novamente mais tarde.")
        
        response = self.get_response(request)
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
