# coding=utf-8
from django.template.defaulttags import register


@register.filter
def get_item(dictionary, key):
    # REF: http://stackoverflow.com/questions/8000022/django-template-how-to-lookup-a-dictionary-value-with-a-variable
    # Usage: handling errors in templates

    return dictionary.get(key)

@register.filter(name='change_word')
def change(value):
    new_vallue=value.replace('\r\n','<br>')
    new_vallue=new_vallue.replace('\n','<br>')
    new_vallue=new_vallue.replace(' ','&nbsp;')
    return new_vallue


@register.filter(name='change_file')
def change_file(value):
    return value.replace(',','<br>')

@register.filter(name='https_status')
def change_https(value):
    if value:
        return u'是'
    else:
        return u'否'
