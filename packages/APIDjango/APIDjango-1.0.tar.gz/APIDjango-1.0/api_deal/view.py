import json

from django.db.models import F
from django.http import QueryDict
from django.utils.decorators import method_decorator
from django.views import View

from . import error
from .args import BaseArgument
from .error import METHOD_NOT_ALLOW
from .page import get_start_end_inx
from .res import SuccessReturn, ErrorReturn


def handle_params(request, *args, **kwargs):
    """处理request的请求参数"""
    if request.method == "GET":
        data = request.GET
    else:
        if request.content_type == "application/json":
            try:
                data = json.loads(request.body)
            except ValueError:
                raise error.ARGUMENT_ERROR("参数解析失败，不是合法的json字符串")
        elif request.content_type == "multipart/form-data":
            data = request.POST
        else:
            data = QueryDict(request.body)
    request.data = data


def decorator(func):
    def wrapper(request, *args, **kwargs):
        handle_params(request, *args, **kwargs)
        try:
            response = func(request, *args, **kwargs)
        except Exception as exc:
            raise exc
        return response

    return wrapper


@method_decorator(decorator, name='dispatch')
class ApiView(View):
    get_params_list = []
    post_params_list = []
    select_put_params_list = []
    put_params_list = []
    delete_params_list = []

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.request = None

    def http_method_not_allowed(self, request, *args, **kwargs):
        return ErrorReturn(METHOD_NOT_ALLOW)

    def check_get_params(self, data):
        for get_param in self.get_params_list:
            if isinstance(get_param, BaseArgument):
                setattr(self, get_param.get_key_name(), get_param.base_check(data))

    def check_post_params(self, data):
        for post_param in self.post_params_list:
            if isinstance(post_param, BaseArgument):
                setattr(self, post_param.get_key_name(), post_param.base_check(data))

    def check_put_params(self, data):
        for param in self.select_put_params_list:
            if isinstance(param, BaseArgument):
                setattr(self, param.get_key_name(), param.base_check(data))
        for param in self.put_params_list:
            if isinstance(param, BaseArgument):
                setattr(self, param.get_key_name(), param.base_check(data))

    def check_delete_params(self, data):
        for param in self.delete_params_list:
            if isinstance(param, BaseArgument):
                setattr(self, param.get_key_name(), param.base_check(data))


class ApiListView(ApiView):
    model = None

    extra = {}
    field_list = []
    field_res = {}
    order_by = None

    def get_query_kwargs(self):
        query_kwargs, _ = self.base_get_kwargs(self.get_params_list)
        real_query_kwargs = {}
        for key, value in query_kwargs.items():
            if value not in ["", None]:
                real_query_kwargs[key] = value
        return real_query_kwargs

    def get_field_kwargs(self):
        field_list = []
        field_res = {}
        for field in self.field_list:
            relate_field = field.get("relate_field", None)
            if relate_field is None:
                field_list.append(field['prop'])
            else:
                field_res[field['prop']] = F(relate_field)
        return field_list, field_res

    def get_data_list(self, data):
        self.check_get_params(data)
        query_kwargs = self.get_query_kwargs()
        field_list, field_res = self.get_field_kwargs()
        data_count = self.model.objects.filter(**query_kwargs).count()
        data_list = self.model.objects.filter(**query_kwargs).extra(**self.extra).values(*field_list, **field_res)
        if self.order_by is not None:
            data_list = data_list.order_by(*self.order_by)
        return data_list, data_count

    def get_header_list(self):
        return [header for header in self.field_list if header.get("is_show", True)]

    def my_get(self, request):
        res = {}
        data_list, data_count = self.get_data_list(request.data)
        start_inx, end_inx = get_start_end_inx(request.data, res, data_count)
        data_list = data_list[start_inx: end_inx]
        res['data_list'] = list(data_list)
        res['header_list'] = self.get_header_list()
        return SuccessReturn(res)

    def base_get_kwargs(self, params_list):
        base_kwargs = {}
        other_kwargs = {}
        for post_param in params_list:
            key = post_param.get_key_name()
            value = getattr(self, post_param.get_key_name(), None)
            is_other_arg = getattr(post_param, "is_other_arg", False)
            if is_other_arg is True:
                other_kwargs[key] = value
            else:
                base_kwargs[key] = value
        return base_kwargs, other_kwargs

    def get_post_kwargs(self):
        return self.base_get_kwargs(self.post_params_list)

    def get_put_select_kwargs(self):
        return self.base_get_kwargs(self.select_put_params_list)

    def get_put_kwargs(self):
        return self.base_get_kwargs(self.put_params_list)

    def my_post(self, request):
        self.check_post_params(request.data)
        create_kwargs, other_kwargs = self.get_post_kwargs()
        self.model.objects.create(**create_kwargs)
        return SuccessReturn()

    def my_put(self, request):
        self.check_put_params(request.data)
        select_put_kwargs, _ = self.get_put_select_kwargs()
        put_kwargs, other_put_kwargs = self.get_put_kwargs()
        self.model.objects.filter(**select_put_kwargs).update(**put_kwargs)
        return SuccessReturn()

    def my_delete(self, request):
        self.check_delete_params(request.data)
        delete_kwargs, other_kwargs = self.base_get_kwargs(self.delete_params_list)
        if not delete_kwargs:
            raise error.ARGUMENT_ERROR("删除条件为空")
        delete_obj_list = self.model.objects.filter(**delete_kwargs)
        count = delete_obj_list.count()
        if count == 0:
            raise error.ARGUMENT_ERROR("删除数量为0")
        delete_obj_list.delete()
        return SuccessReturn()
