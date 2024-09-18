from django.http import JsonResponse


def heath_check_view(request):  # noqa
    return JsonResponse({"status": "ok"})
