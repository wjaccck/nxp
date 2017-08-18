# #coding=utf8
from django_select2.forms import (
    HeavySelect2MultipleWidget, HeavySelect2Widget, ModelSelect2MultipleWidget,
    ModelSelect2TagWidget, ModelSelect2Widget, Select2MultipleWidget,
    Select2Widget
)

class BaseSearchFieldMixin(object):
    pass

class BaseModelSelect2MultipleWidget(BaseSearchFieldMixin, ModelSelect2MultipleWidget):
    pass

class BaseModelSelect2Widget(BaseSearchFieldMixin, ModelSelect2Widget):
    pass

class ModelSelect2Widget(BaseModelSelect2Widget):
    search_fields = [
        'name__istartswith',
        'pk__startswith',
    ]

class ModelSelect2MultipleWidget(BaseModelSelect2MultipleWidget):
    search_fields = [
        'name__istartswith',
        'pk__startswith',
    ]

class GroupModelSelect2Widget(BaseModelSelect2Widget):
    search_fields = [
        'name__istartswith',
        'pk__startswith',
    ]

class UpstreamModelSelect2MultipleWidget(BaseModelSelect2MultipleWidget):
    search_fields = [
        'name__istartswith',
        'pk__startswith',
    ]

class SiteModelSelect2Widget(BaseModelSelect2Widget):
    search_fields = [
        'name__istartswith',
        'pk__startswith',
    ]

class UpstreamSelect2Widget(BaseModelSelect2Widget):
    search_fields = [
        'name__istartswith',
        'pk__startswith',
    ]

class Redis_instanceSelect2Widget(BaseModelSelect2Widget):
    search_fields = [
        'name__istartswith',
        'pk__startswith',
    ]

class Redis_instanceMultipleWidget(BaseModelSelect2MultipleWidget):
    search_fields = [
        'name__istartswith',
        'pk__startswith',
    ]

class Redis_groupMultipleWidget(BaseModelSelect2MultipleWidget):
    search_fields = [
        'name__istartswith',
        'pk__startswith',
    ]