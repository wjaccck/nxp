from rest_framework.pagination import PageNumberPagination


class DefaultResultsSetPagination(PageNumberPagination):
    '''
    A customized pagination class.
    REF: http://www.django-rest-framework.org/api-guide/pagination/#modifying-the-pagination-style
    '''
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 2000

