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
                ('next_page', self.get_next_page_number()),
                ('previous_page', self.get_previous_page_number()),
                ('total_page', self.page.paginator.num_pages)
            ])),
            ('data', data)
        ]))

    def get_previous_page_number(self):
        if not self.page.has_previous():
            return None
        return self.page.previous_page_number()

    def get_next_page_number(self):
        if not self.page.has_next():
            return None
        return self.page.next_page_number()


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
