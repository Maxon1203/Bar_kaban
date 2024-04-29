from django import template

# Регистрация собственных шаблонов тега
register = template.Library()

@register.simple_tag
def header_link(curr_page, state):
    if curr_page == state:
        return 'nav-item nav-link link-body-emphasis active'
    return 'nav-item nav-link link-body-emphasis'
