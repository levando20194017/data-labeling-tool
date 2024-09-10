from django.http import JsonResponse

class TokenAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Kiểm tra xem yêu cầu có được gửi tới URL của Swagger không
        if request.path.startswith('/api/schema/docs/'):  # Thay đổi đoạn này để phù hợp với URL của Swagger
            response = self.get_response(request)
        else:
            # Đoạn mã kiểm tra token ở đây
            access_token = request.META.get('HTTP_AUTHORIZATION')

            if not access_token:
                return JsonResponse({'error': 'Authorization token missing'}, status=401)

            # Thực hiện xác thực token ở đây

            response = self.get_response(request)

        return response