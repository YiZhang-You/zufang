from rest_framework.pagination import PageNumberPagination, CursorPagination


class CustomPagePagination(PageNumberPagination):
    page_size_query_param = 'size'
    max_page_size = 50


class AgentCursorPagination(CursorPagination):
    page_size_query_param = 'size'
    max_page_size = 50
    ordering = 'agentid'
