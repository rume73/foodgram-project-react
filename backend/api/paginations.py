from rest_framework.pagination import PageNumberPagination


class PageNumberPaginatorModified(PageNumberPagination):
    page_size_query_param = 'limit'
