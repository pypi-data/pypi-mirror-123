from django.db.models import Func, Value, CharField


class MySQL_DATETIME_FORMAT(Func):
    function = 'DATE_FORMAT'
    arity = 2


class MySQL_IfNull(Func):
    function = 'IFNULL'
    arity = 2


class MySQL_If(Func):
    function = "IF"


class MySQL_FIELD_IS_NOT_NULL(Func):
    function = "IS NOT NULL"
    template = '(%(expressions)s)%(function)s'
    arity = 1


def change_mysql_datetime_to_str(field, format_type="datetime"):
    if format_type == "date":
        field_format = "%Y-%m-%d"
    elif format_type == "time":
        field_format = "%H:%i:%s"
    else:
        field_format = "%Y-%m-%d %H:%i:%s"
    return MySQL_DATETIME_FORMAT(field, Value(field_format), output_field=CharField())
