import sys

from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request


class ApiPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'per_page'

    def get_page_size(self, request: Request) -> int:
        if request.query_params.get(self.page_size_query_param) == 'all':
            return sys.maxsize
        return super().get_page_size(request)
