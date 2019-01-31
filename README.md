[TOC]


# pagination

## #0 Blog

```
https://blog.csdn.net/Coxhuang/article/details/86728147
```

## #1 环境

```
Python3.6
Django==2.0.7
djangorestframework==3.8.2
```


## #2 需求分析
- 查看某个列表式,需要分页展示
- 自定义分页输出的格式
- 自定义分页的参数

## #3 开始

### #3.1 新建一个Django项目
### #3.2 新建文件 pagination.py(文件名随意)

```
from rest_framework.pagination  import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class MyCustomPagination(PageNumberPagination):
   
    page_size = 5 # 每页显示多少个

    page_size_query_param = "size" # 默认每页显示3个，可以通过传入pager1/?page=2&size=4,改变默认每页显示的个数

    max_page_size = 100 # 最大页数不超过100

    page_query_param = "page" # 获取页码数的

    def get_paginated_response(self, data):
        """输出格式"""
        return Response(OrderedDict([
            ('count', self.page.paginator.count), # 整个数据的个数
            ('success', True), # 验证消息
            ('next', self.get_next_link()), # 下一页url
            ('previous', self.get_previous_link()), # 上一页url
            ('results', data) # 当前页的数据
         ]))


```

### #3.3 使用
#### #3.3.1 没有使用分页

**视图**
```

class get_view(mixins.CreateModelMixin,
               mixins.ListModelMixin,
               GenericViewSet):
    pagination_class = None # 没有使用分页(也可以注释掉)

    queryset = models.Student.objects.all()
    serializer_class = get_sreializer
    
```

**接口数据**
```
[
    {
        "id": 1,
        "name": "cox",
        "age": "12"
    },
    {
        "id": 2,
        "name": "cox",
        "age": "12"
    },
    {
        "id": 3,
        "name": "cox",
        "age": "12"
    },
    {
        "id": 4,
        "name": "cox",
        "age": "12"
    },
    
    ...
    ...
    ...
]
```
#### #3.3.2 使用分页

**视图**


```
from app.pagination import MyCustomPagination
class get_view(mixins.CreateModelMixin,
               mixins.ListModelMixin,
               GenericViewSet):
    pagination_class = MyCustomPagination # 使用刚刚自定义的分页

    queryset = models.Student.objects.all()
    serializer_class = get_sreializer
```

**接口数据**


```
{
    "count": 11,
    "success": true,
    "next": "http://127.0.0.1:8000/get_data/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "cox",
            "age": "12"
        },
        {
            "id": 2,
            "name": "cox",
            "age": "12"
        },
        {
            "id": 3,
            "name": "cox",
            "age": "12"
        },
        {
            "id": 4,
            "name": "cox",
            "age": "12"
        },
        {
            "id": 5,
            "name": "cox",
            "age": "12"
        }
    ]
}
```

### #3.4 如果有的接口需要显示与其他接口数量不同的数据,该怎么办

需求:
- A接口,分页显示 5 条数据
- B接口,每页显示 5 条数据
- ...
- ...
- Z接口,每页显示 100000 条数据

如何处理Z接口

尝试:
- 在Z接口中, 重新定义 page_size = 100000,这样调用分页是,就会覆盖之前的 page_size; (事实证明,这样子不行的)
- 集成自定义分页类,在子类中重新定义page_size = 100000,在Z接口中 pagination_class = 子类; (完美)


**视图**
```
from app.pagination import MyCustomPagination

class MyChildCustomPagination(MyCustomPagination):

    page_size = 1 # 每页显示多少个

class get_view(mixins.CreateModelMixin,
               mixins.ListModelMixin,
               GenericViewSet):
    pagination_class = MyChildCustomPagination # 子类

    queryset = models.Student.objects.all()
    serializer_class = get_sreializer
```

**接口数据**


```
{
    "count": 11,
    "success": true,
    "next": "http://127.0.0.1:8000/get_data/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "cox",
            "age": "12"
        }
    ]
}
```






