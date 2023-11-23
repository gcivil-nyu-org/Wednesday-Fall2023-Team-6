from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(my_list, index):
    try:
        return my_list[index]
    except IndexError:
        return None
