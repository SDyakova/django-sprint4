from django.shortcuts import render


def page_not_found(request, exception):
    """Страница 404 (не найдено)"""
    return render(request, "pages/404.html", status=404)


def csrf_failure(request, reason=""):
    """Страница 403 CSRF (ошибка токена)"""
    return render(request, "pages/403csrf.html", status=403)


def server_error(request):
    """Страница 500 (ошибка сервера)"""
    return render(request, "pages/500.html", status=500)
