import markdown
from django import template
from django.utils.safestring import mark_safe
register = template.Library()
import re

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
    try:
        value = int(value)
    except ValueError:
        return value  # 값이 정수가 아닌 경우 그대로 반환
    return "{:,}".format(value)

@register.filter
def add_commas2(value):
    # 입력값에서 숫자와 .만 남기고 모두 제거합니다.
    num = re.sub(r'\D', '', value)
    
    # 천 단위마다 쉼표를 추가합니다.
    return re.sub(r'\B(?=(\d{3})+(?!\d))', ',', num)
# 버림
@register.filter
def truncate_decimal(value):
    return int(value)

# 부동 소수점 변환
@register.filter
def to_float(value):
    return float(value)

# 부동 소수점 변환
@register.filter
def to_str(value):
    return str(value)