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

