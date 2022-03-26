# """
# Generates Link Preview
# """
from django.utils import html
from django import template

import content

register = template.Library()
@register.simple_tag
def link_li(article_name):
    """
    Needs better description
    """
    title, subtitle, desc, img = content.get_summary(article_name)
    href = '/article/hi/' + article_name
    return html.format_html(f"""
        <a class='linkpreview' href='{href}'>
        <img style='float:left;width:100px;' src='{img}'/>
        <div>
            <div style="font-size:1em;">{title}</div>
            <div style="color: silver;font-size:0.75em;">{subtitle}</div>
            <div style="color: silver;font-size:0.75em;">{desc}</div>
        </div>
        </a>
    """ % locals())
