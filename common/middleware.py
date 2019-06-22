from django.utils.deprecation import MiddlewareMixin


class NotloginMiddleware(MiddlewareMixin):
    def process_request(self, request):
        pass

    def process_view(self, request, callback, callback_args, callback_kwargs):
        pass

    def process_response(self, request, response):
        return response
