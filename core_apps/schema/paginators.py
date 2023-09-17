from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from collections import OrderedDict


class MyBasePagination(PageNumberPagination):
    page_size_query_param = "pageSize"
    max_page_size = 1000
    page_query_param = "page"
    last_page_strings = ("last", "end",)
    page_size = 100

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('pageable', OrderedDict([
                ('size', self.page.paginator.count),
                ('next_page', self.get_next_link()),
                ('previous_page', self.get_previous_link())
            ])),
            ('data', data)
        ]))


class SmallSizePagination(MyBasePagination):
    page_size = 20
    max_page_size = 50


class MediumSizePagination(MyBasePagination):
    page_size = 100
    max_page_size = 500


class LargeSizePagination(MyBasePagination):
    page_size = 1000
    max_page_size = 5000


class SuperLargeSizePagination(MyBasePagination):
    page_size = 10000
    max_page_size = 50000
