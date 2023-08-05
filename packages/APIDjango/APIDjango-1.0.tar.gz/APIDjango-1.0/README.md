# django_api_deal

#### 打包命令
```angular2html
python setup.py sdist
```
#### 上传命令   
```angular2html
twine upload dist/*
```
#### 主要功能

1. 简化常见列表类接口
    1. get、post、put、delete都有对应的my_get、my_post、my_put、my_delete方法。
2. 简化参数的校验及检验失败的提示信息
   1. 参数类型
      1. StrArgument 字符串参数
      2. StrOfIntArgument 整形的字符串参数
      3. EmailArgument 邮箱参数 必须有@
      4. UrlArgument url参数 必须http 或 https开头
      5. ListArgument 列表参数
      6. DictArgument 字典参数
      7. ListNestDictArgument 列表嵌套字典参数 可多层嵌套
      8. ChoiceArgument 固定可选值参数 一般用来 True, False，或者其他固定可选项
      9. BoolArgument bool参数
      10. StrOfBoolArgument bool类型的字符串参数
      11. DateStrArgument 日期参数，可自定义日期格式 datetime_format
      12. IntArgument FloatArgument DecimalArgument
   2.简化参数的参数
      13. desc 名称 
      14. name 上传字段名称 
      15. must 是否必填 
      16. query_type 查询时的方式：icontains 
      17. relate_name 查询字段与name字段不一致时使用或关联查询时使用


4. core跨域解决
   1. 在settings中的中间件增加下面的代码

   ```angular2html
   'api_deal.middlewares.cors.MyCorsMiddleware', 
   ```

5. 通用的异常处理
   1. 在settings中的中间件增加下面的代码

      ```angular2html
         'api_deal.middlewares.error.MyErrorMiddleware',
      ```

代码示例：

```angular2html

class BookListView(ApiListView):
    model = Book
    id_arg = IntArgument("ID", "id", must=True)
    name_arg = StrArgument("名称", "name", must=True, query_type="icontains", )
    get_params_list = [
        name_arg,
    ]

    def get(self, request):
        return self.my_get(request)

    post_params_list = [
        name_arg,
    ]

    def post(self, request):
        return self.my_post(request)

    select_put_params_list = [
        id_arg,
    ]
    put_params_list = [
        name_arg,
    ]

    def put(self, request):
        return self.my_put(request)

    delete_params_list = [
        id_arg
    ]

    def delete(self, request):
        return self.my_delete(request)

```

正确返回示例
```angular2html
{
    "errmsg": "ok"
    "data": {...}
}
```

错误返回示例
```
{
    "errmsg": "参数名称是必填项"
    "data": null
}
```