from django.shortcuts import render


# HTTP Error 403
def custom_page_not_found_view(request, exception):
    return render(request, "maintenance/page-404.html", {})

def custom_error_view(request, exception=None):
    return render(request, "maintenance/page-500.html", {})

def custom_permission_denied_view(request, exception=None):
    return render(request, "maintenance/page-403.html", {})

# def custom_bad_request_view(request, exception=None):
#     return render(request, "errors/400.html", {})