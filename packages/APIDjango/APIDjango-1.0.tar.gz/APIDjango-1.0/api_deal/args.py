import datetime
from decimal import Decimal

from . import error


class BaseArgument(object):
    must = False  # 参数是否必填
    name = ""  # 参数名称
    type = None  # 参数类型
    value_type = None  # 值类型
    desc = ""  # 参数详细信息
    is_other_arg = False  # 是否其他对象参数
    value = None
    f = {}

    def __init__(self, desc, name, must=False, query_type=None, relate_name=None, is_other_arg=False):
        self.desc = desc
        self.name = name
        self.must = must
        self.query_type = query_type
        self.relate_name = relate_name
        self.is_other_arg = is_other_arg
        if self.value_type is None:
            self.value_type = self.type

    def base_check(self, data):
        value = data.get(self.name)
        if self.must:
            if self.name not in data.keys():
                raise error.ARGUMENT_ERROR("缺少{field_name}参数".format(field_name=self.name))
            if not value and not (value is False or value == [] or value == {}):
                raise error.ARGUMENT_ERROR("{field_name}值不能为空".format(field_name=self.name))
        self.f = {"field_name": self.name, "field_type": self.type, "value_type": type(value)}
        if self.type is None:
            return value
        if value and not isinstance(value, self.type):
            raise error.ARGUMENT_ERROR("{field_name}期望是： {field_type}，实际是： {value_type}".format(**self.f))
        return value

    def get_key_name(self):
        key_name = self.name
        if self.relate_name:
            key_name = self.relate_name
        if self.query_type:
            key_name = "__".join([key_name, self.query_type])
        return key_name

    def __str__(self):
        return "-".join([self.desc, self.name, str(self.must)])


class IntArgument(BaseArgument):
    type = int


class FloatArgument(BaseArgument):
    type = float

    def __init__(self, desc, name, must=False, decimal_places=2):
        super().__init__(desc, name, must)
        self.decimal_places = decimal_places

    def base_check(self, data):
        value = data.get(self.name)
        if value:
            try:
                value = float(value)
            except:
                raise error.ARGUMENT_ERROR("{field_name}参数类型错误".format(field_name=self.name))
        data[self.name] = value
        super().base_check(data)
        return round(value, self.decimal_places)


class DecimalArgument(FloatArgument):
    type = Decimal

    def base_check(self, data):
        value = data.get(self.name)
        if value:
            try:
                value = Decimal(value).quantize(Decimal("0." + "0" * self.decimal_places))
            except:
                raise error.ARGUMENT_ERROR("{field_name}参数类型错误".format(field_name=self.name))
        data[self.name] = value
        super().base_check(data)
        return value


class StrArgument(BaseArgument):
    type = str


class StrOfIntArgument(BaseArgument):
    """数字类型的字符串"""
    type = str
    value_type = int

    def base_check(self, data):
        value = super().base_check(data)
        if value:
            try:
                value = int(value)
            except:
                raise error.ARGUMENT_ERROR("{field_name}类型错误".format(field_name=self.name))
        return value


class EmailArgument(StrArgument):

    def base_check(self, data):
        value = super().base_check(data)
        if value and value.find("@") == -1:
            raise error.ARGUMENT_ERROR("邮箱格式不正确")
        return value


class UrlArgument(StrArgument):

    def base_check(self, data):
        value = super().base_check(data)
        if value:
            if not (value.startswith("http") or value.startswith("//")):
                raise error.ARGUMENT_ERROR("{name}格式不正确".format(name=self.name))
        return value


class ListArgument(BaseArgument):
    type = list


class DictArgument(BaseArgument):
    type = dict

    def __init__(self, desc, name, must=False, dict_arg_list=None, ):
        super().__init__(desc, name, must)
        self.dict_arg_list = dict_arg_list

    def base_check(self, data):
        value = super().base_check(data)
        result = {}
        for dict_arg in self.dict_arg_list:
            v_v = dict_arg.base_check(value)
            result[dict_arg.get_key_name()] = v_v
        return result


class ListNestDictArgument(ListArgument):
    dict_arg_list = None  # 只判断最外层key值

    def __init__(self, desc, name, must=False, is_other_arg=False, dict_arg_list=None, ):
        super().__init__(desc=desc, name=name, must=must, is_other_arg=is_other_arg)
        self.dict_arg_list = dict_arg_list

    def base_check(self, data):
        value = super().base_check(data)
        result = []
        if not [False for i in [self.dict_arg_list, value] if not isinstance(i, self.type)]:
            for v in value:
                one = {}
                for dict_arg in self.dict_arg_list:
                    v_v = dict_arg.base_check(v)
                    one[dict_arg.get_key_name()] = v_v
                result.append(one)
        return result


class ChoiceArgument(BaseArgument):
    type = str
    choice_list = None

    def __init__(self, desc, name, must=False, choice_list=None, relate_name=None):
        super().__init__(desc, name, must, relate_name=relate_name)
        self.choice_list = choice_list

    def base_check(self, data):
        value = super().base_check(data)
        if isinstance(self.choice_list, tuple) or isinstance(self.choice_list, list):
            if self.must and value not in self.choice_list:
                self.f['choices'] = ";".join(self.choice_list)
                raise error.ARGUMENT_ERROR("{field_name}超出允许的范围：{choices}".format(**self.f))
        return value


class BoolArgument(ChoiceArgument):
    type = bool
    choice_list = (True, False)

    def __init__(self, desc, name, must=False, relate_name=None):
        super().__init__(desc, name, must=must, choice_list=self.choice_list, relate_name=relate_name)


class StrOfBoolArgument(BoolArgument):
    type = str
    value_type = bool
    choice_list = ("true", "false")

    def base_check(self, data):
        value = super().base_check(data)
        if value == "true":
            value = True
        elif value == "false":
            value = False
        else:
            value = None
        return value


class DateStrArgument(StrArgument):
    type = str
    datetime_format = None

    def __init__(self, desc, name, must=False, query_type=None, relate_name=None, datetime_format="%Y-%m-%d"):
        super().__init__(desc, name, must, query_type, relate_name)
        self.datetime_format = datetime_format

    def base_check(self, data):
        value = super().base_check(data)
        if value:
            try:
                _ = datetime.datetime.strptime(value, self.datetime_format)
            except Exception as e:
                raise error.ARGUMENT_ERROR("日期格式不正确")
        return value
