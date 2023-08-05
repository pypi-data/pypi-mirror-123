from django.http import JsonResponse


def BaseReturn(return_data, status=200):
    return JsonResponse(return_data, status=status)


def SuccessReturn(data=None):
    if data is None:
        data = {}
    return_data = {
        "errmsg": "ok",
        "data": data,
    }
    return BaseReturn(return_data)


def ErrorReturn(my_error):
    return_data = {
        "errmsg": my_error.errmsg,
        "data": None,
    }
    return BaseReturn(return_data, status=my_error.code)
