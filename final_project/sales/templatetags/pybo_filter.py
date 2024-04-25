import markdown
from django import template
from django.utils.safestring import mark_safe
register = template.Library()


@register.filter
def sub(value, arg):
    return value - arg

@register.filter
def mark(value):
    extensions = ["nl2br", "fenced_code"]
    return mark_safe(markdown.markdown(value, extensions=extensions))

# 자릿수 추가
@register.filter
def add_commas(value):
    return "{:,}".format(value)

# 버림
@register.filter
def truncate_decimal(value):
    return int(value)

# 부동 소수점 변환
@register.filter
def to_float(value):
    return float(value)