import time
from django.http import HttpResponseForbidden, HttpResponse
from django.core.cache import cache
from django.conf import settings

class DisableHTTPSRedirectMiddleware:
    """
    Middleware para desabilitar completamente qualquer redirecionamento para HTTPS.
    Isso é necessário apenas em ambiente de desenvolvimento, já que o servidor
    de desenvolvimento do Django não suporta HTTPS.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Processa a resposta normalmente
        response = self.get_response(request)
        
        # Se estamos em modo de desenvolvimento e a resposta é um redirecionamento para HTTPS
        if settings.DEBUG and response.status_code == 301 and response.get('Location', '').startswith('https'):
            # Substitui o redirecionamento HTTPS por HTTP
            url = response['Location'].replace('https://', 'http://')
            return HttpResponse(
                f'<html><body>Redirecionamento para HTTPS detectado e bloqueado.<br>'
                f'Por favor, acesse <a href="{url}">{url}</a> diretamente.</body></html>'
            )
        
        # Remove qualquer cabeçalho relacionado a HTTPS
        if settings.DEBUG:
            if 'Strict-Transport-Security' in response:
                del response['Strict-Transport-Security']
        
        return response


class RateLimitMiddleware:
    """
    Middleware para limitar tentativas de login baseado no endereço IP.
    Isso ajuda a prevenir ataques de força bruta.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if (request.path == '/accounts/login/' or request.path == '/login/') and request.method == 'POST':
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
