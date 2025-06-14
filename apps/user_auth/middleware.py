class CustomHeadersMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.user.is_authenticated:
            response['X-Django-User'] = request.user.id
        return  response


def company(company_id:str):
    return  company_id + str(10)
