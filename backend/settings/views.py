from django.http import HttpResponse  # http response class

# arg http client request return response object
# html string as content
def hello(request):  # request required first arg in view function
    return HttpResponse(
    '<h1>Hello ERP Backend</h1>'
    )